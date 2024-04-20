# Copyright Modal Labs 2023
import asyncio
import inspect
import time
import typing
import warnings
from contextvars import ContextVar
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import (
    TYPE_CHECKING,
    Any,
    AsyncGenerator,
    AsyncIterable,
    AsyncIterator,
    Callable,
    Collection,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Set,
    Sized,
    Tuple,
    Type,
    Union,
)

from aiostream import pipe, stream
from google.protobuf.message import Message
from grpclib import GRPCError, Status
from synchronicity.combined_types import MethodWithAio
from synchronicity.exceptions import UserCodeException

from modal_proto import api_grpc, api_pb2

from ._container_io_manager import is_local
from ._location import parse_cloud_provider
from ._output import OutputManager
from ._pty import get_pty_info
from ._resolver import Resolver
from ._resources import convert_fn_config_to_resources_config
from ._serialization import deserialize, deserialize_data_format, serialize
from ._traceback import append_modal_tb
from ._utils.async_utils import (
    AsyncOrSyncIteratable,
    queue_batch_iterator,
    synchronize_api,
    synchronizer,
    warn_if_generator_is_not_consumed,
)
from ._utils.blob_utils import (
    BLOB_MAX_PARALLELISM,
    MAX_OBJECT_SIZE_BYTES,
    blob_download,
    blob_upload,
)
from ._utils.function_utils import FunctionInfo, _stream_function_call_data, get_referred_objects, is_async
from ._utils.grpc_utils import retry_transient_errors
from ._utils.mount_utils import validate_mount_points, validate_volumes
from .call_graph import InputInfo, _reconstruct_call_graph
from .client import _Client
from .cloud_bucket_mount import _CloudBucketMount, cloud_bucket_mounts_to_proto
from .config import config, logger
from .exception import (
    ExecutionError,
    FunctionTimeoutError,
    InvalidError,
    NotFoundError,
    RemoteError,
    deprecation_warning,
)
from .gpu import GPU_T, parse_gpu_config
from .image import _Image
from .mount import _get_client_mount, _Mount
from .network_file_system import _NetworkFileSystem, network_file_system_mount_protos
from .object import Object, _get_environment_name, _Object, live_method, live_method_gen
from .proxy import _Proxy
from .retries import Retries
from .schedule import Schedule
from .scheduler_placement import SchedulerPlacement
from .secret import _Secret
from .volume import _Volume

OUTPUTS_TIMEOUT = 55.0  # seconds
ATTEMPT_TIMEOUT_GRACE_PERIOD = 5  # seconds


if TYPE_CHECKING:
    import modal.app


class _SynchronizedQueue:
    """mdmd:hidden"""

    # small wrapper around asyncio.Queue to make it cross-thread compatible through synchronicity
    async def init(self):
        # in Python 3.8 the asyncio.Queue is bound to the event loop on creation
        # so it needs to be created in a synchronicity-wrapped init method
        self.q = asyncio.Queue()

    @synchronizer.no_io_translation
    async def put(self, item):
        await self.q.put(item)

    @synchronizer.no_io_translation
    async def get(self):
        return await self.q.get()


SynchronizedQueue = synchronize_api(_SynchronizedQueue)


def exc_with_hints(exc: BaseException):
    """mdmd:hidden"""
    if isinstance(exc, ImportError) and exc.msg == "attempted relative import with no known parent package":
        exc.msg += """\n
HINT: For relative imports to work, you might need to run your modal app as a module. Try:
- `python -m my_pkg.my_app` instead of `python my_pkg/my_app.py`
- `modal deploy my_pkg.my_app` instead of `modal deploy my_pkg/my_app.py`
"""
    elif isinstance(
        exc, RuntimeError
    ) and "CUDA error: no kernel image is available for execution on the device" in str(exc):
        msg = (
            exc.args[0]
            + """\n
HINT: This error usually indicates an outdated CUDA version. Older versions of torch (<=1.12)
come with CUDA 10.2 by default. If pinning to an older torch version, you can specify a CUDA version
manually, for example:
-  image.pip_install("torch==1.12.1+cu116", find_links="https://download.pytorch.org/whl/torch_stable.html")
"""
        )
        exc.args = (msg,)

    return exc


async def _process_result(result: api_pb2.GenericResult, data_format: int, stub, client=None):
    if result.WhichOneof("data_oneof") == "data_blob_id":
        data = await blob_download(result.data_blob_id, stub)
    else:
        data = result.data

    if result.status == api_pb2.GenericResult.GENERIC_STATUS_TIMEOUT:
        raise FunctionTimeoutError(result.exception)
    elif result.status != api_pb2.GenericResult.GENERIC_STATUS_SUCCESS:
        if data:
            try:
                exc = deserialize(data, client)
            except Exception as deser_exc:
                raise ExecutionError(
                    "Could not deserialize remote exception due to local error:\n"
                    + f"{deser_exc}\n"
                    + "This can happen if your local environment does not have the remote exception definitions.\n"
                    + "Here is the remote traceback:\n"
                    + f"{result.traceback}"
                )
            if not isinstance(exc, BaseException):
                raise ExecutionError(f"Got remote exception of incorrect type {type(exc)}")

            if result.serialized_tb:
                try:
                    tb_dict = deserialize(result.serialized_tb, client)
                    line_cache = deserialize(result.tb_line_cache, client)
                    append_modal_tb(exc, tb_dict, line_cache)
                except Exception:
                    pass
            uc_exc = UserCodeException(exc_with_hints(exc))
            raise uc_exc
        raise RemoteError(result.exception)

    try:
        return deserialize_data_format(data, data_format, client)
    except ModuleNotFoundError as deser_exc:
        raise ExecutionError(
            "Could not deserialize result due to error:\n"
            + f"{deser_exc}\n"
            + "This can happen if your local environment does not have a module that was used to construct the result. \n"
        )


async def _create_input(args, kwargs, client, idx: Optional[int] = None) -> api_pb2.FunctionPutInputsItem:
    """Serialize function arguments and create a FunctionInput protobuf,
    uploading to blob storage if needed.
    """
    if idx is None:
        idx = 0

    args_serialized = serialize((args, kwargs))

    if len(args_serialized) > MAX_OBJECT_SIZE_BYTES:
        args_blob_id = await blob_upload(args_serialized, client.stub)

        return api_pb2.FunctionPutInputsItem(
            input=api_pb2.FunctionInput(args_blob_id=args_blob_id, data_format=api_pb2.DATA_FORMAT_PICKLE),
            idx=idx,
        )
    else:
        return api_pb2.FunctionPutInputsItem(
            input=api_pb2.FunctionInput(args=args_serialized, data_format=api_pb2.DATA_FORMAT_PICKLE),
            idx=idx,
        )


@dataclass
class _OutputValue:
    # box class for distinguishing None results from non-existing/None markers
    value: Any


class _Invocation:
    """Internal client representation of a single-input call to a Modal Function or Generator"""

    def __init__(self, stub: api_grpc.ModalClientStub, function_call_id: str, client: _Client):
        self.stub = stub
        self.client = client  # Used by the deserializer.
        self.function_call_id = function_call_id  # TODO: remove and use only input_id

    @staticmethod
    async def create(function_id: str, args, kwargs, client: _Client) -> "_Invocation":
        assert client.stub
        item = await _create_input(args, kwargs, client)

        request = api_pb2.FunctionMapRequest(
            function_id=function_id,
            parent_input_id=current_input_id() or "",
            function_call_type=api_pb2.FUNCTION_CALL_TYPE_UNARY,
            pipelined_inputs=[item],
        )
        response = await retry_transient_errors(client.stub.FunctionMap, request)
        function_call_id = response.function_call_id

        if response.pipelined_inputs:
            return _Invocation(client.stub, function_call_id, client)

        request_put = api_pb2.FunctionPutInputsRequest(
            function_id=function_id, inputs=[item], function_call_id=function_call_id
        )
        inputs_response: api_pb2.FunctionPutInputsResponse = await retry_transient_errors(
            client.stub.FunctionPutInputs,
            request_put,
        )
        processed_inputs = inputs_response.inputs
        if not processed_inputs:
            raise Exception("Could not create function call - the input queue seems to be full")
        return _Invocation(client.stub, function_call_id, client)

    async def pop_function_call_outputs(
        self, timeout: Optional[float], clear_on_success: bool
    ) -> AsyncIterator[api_pb2.FunctionGetOutputsItem]:
        t0 = time.time()
        if timeout is None:
            backend_timeout = OUTPUTS_TIMEOUT
        else:
            backend_timeout = min(OUTPUTS_TIMEOUT, timeout)  # refresh backend call every 55s

        while True:
            # always execute at least one poll for results, regardless if timeout is 0
            request = api_pb2.FunctionGetOutputsRequest(
                function_call_id=self.function_call_id,
                timeout=backend_timeout,
                last_entry_id="0-0",
                clear_on_success=clear_on_success,
            )
            response: api_pb2.FunctionGetOutputsResponse = await retry_transient_errors(
                self.stub.FunctionGetOutputs,
                request,
                attempt_timeout=backend_timeout + ATTEMPT_TIMEOUT_GRACE_PERIOD,
            )
            if len(response.outputs) > 0:
                for item in response.outputs:
                    yield item
                return

            if timeout is not None:
                # update timeout in retry loop
                backend_timeout = min(OUTPUTS_TIMEOUT, t0 + timeout - time.time())
                if backend_timeout < 0:
                    break

    async def run_function(self) -> Any:
        # waits indefinitely for a single result for the function, and clear the outputs buffer after
        item: api_pb2.FunctionGetOutputsItem = (
            await stream.list(self.pop_function_call_outputs(timeout=None, clear_on_success=True))
        )[0]
        assert not item.result.gen_status
        return await _process_result(item.result, item.data_format, self.stub, self.client)

    async def poll_function(self, timeout: Optional[float] = None):
        """Waits up to timeout for a result from a function.

        If timeout is `None`, waits indefinitely. This function is not
        cancellation-safe.
        """
        items: List[api_pb2.FunctionGetOutputsItem] = await stream.list(
            self.pop_function_call_outputs(timeout=timeout, clear_on_success=False)
        )

        if len(items) == 0:
            raise TimeoutError()

        return await _process_result(items[0].result, items[0].data_format, self.stub, self.client)

    async def run_generator(self):
        data_stream = _stream_function_call_data(self.client, self.function_call_id, variant="data_out")
        combined_stream = stream.merge(data_stream, stream.call(self.run_function))  # type: ignore

        items_received = 0
        items_total: Union[int, None] = None  # populated when self.run_function() completes
        async with combined_stream.stream() as streamer:
            async for item in streamer:
                if isinstance(item, api_pb2.GeneratorDone):
                    items_total = item.items_total
                else:
                    yield item
                    items_received += 1
                # The comparison avoids infinite loops if a non-deterministic generator is retried
                # and produces less data in the second run than what was already sent.
                if items_total is not None and items_received >= items_total:
                    break


MAP_INVOCATION_CHUNK_SIZE = 49


async def _map_invocation(
    function_id: str,
    raw_input_queue: _SynchronizedQueue,
    client: _Client,
    order_outputs: bool,
    return_exceptions: bool,
    count_update_callback: Optional[Callable[[int, int], None]],
):
    assert client.stub
    request = api_pb2.FunctionMapRequest(
        function_id=function_id,
        parent_input_id=current_input_id() or "",
        function_call_type=api_pb2.FUNCTION_CALL_TYPE_MAP,
        return_exceptions=return_exceptions,
    )
    response = await retry_transient_errors(client.stub.FunctionMap, request)

    function_call_id = response.function_call_id

    have_all_inputs = False
    num_inputs = 0
    num_outputs = 0

    def count_update():
        if count_update_callback is not None:
            count_update_callback(num_outputs, num_inputs)

    pending_outputs: Dict[str, int] = {}  # Map input_id -> next expected gen_index value
    completed_outputs: Set[str] = set()  # Set of input_ids whose outputs are complete (expecting no more values)

    input_queue: asyncio.Queue = asyncio.Queue()

    async def create_input(argskwargs):
        nonlocal num_inputs
        idx = num_inputs
        num_inputs += 1
        (args, kwargs) = argskwargs
        return await _create_input(args, kwargs, client, idx)

    async def input_iter():
        while 1:
            raw_input = await raw_input_queue.get()
            if raw_input is None:  # end of input sentinel
                return
            yield raw_input  # args, kwargs

    async def drain_input_generator():
        # Parallelize uploading blobs
        proto_input_stream = stream.iterate(input_iter()) | pipe.map(
            create_input,  # type: ignore[reportArgumentType]
            ordered=True,
            task_limit=BLOB_MAX_PARALLELISM,
        )
        async with proto_input_stream.stream() as streamer:
            async for item in streamer:
                await input_queue.put(item)

        # close queue iterator
        await input_queue.put(None)
        yield

    async def pump_inputs():
        assert client.stub
        nonlocal have_all_inputs, num_inputs
        async for items in queue_batch_iterator(input_queue, MAP_INVOCATION_CHUNK_SIZE):
            request = api_pb2.FunctionPutInputsRequest(
                function_id=function_id, inputs=items, function_call_id=function_call_id
            )
            logger.debug(
                f"Pushing {len(items)} inputs to server. Num queued inputs awaiting push is {input_queue.qsize()}."
            )
            resp = await retry_transient_errors(
                client.stub.FunctionPutInputs,
                request,
                max_retries=None,
                max_delay=10,
                additional_status_codes=[Status.RESOURCE_EXHAUSTED],
            )
            count_update()
            for item in resp.inputs:
                pending_outputs.setdefault(item.input_id, 0)
            logger.debug(
                f"Successfully pushed {len(items)} inputs to server. Num queued inputs awaiting push is {input_queue.qsize()}."
            )

        have_all_inputs = True
        yield

    async def get_all_outputs():
        assert client.stub
        nonlocal num_inputs, num_outputs, have_all_inputs
        last_entry_id = "0-0"
        while not have_all_inputs or len(pending_outputs) > len(completed_outputs):
            request = api_pb2.FunctionGetOutputsRequest(
                function_call_id=function_call_id,
                timeout=OUTPUTS_TIMEOUT,
                last_entry_id=last_entry_id,
                clear_on_success=False,
            )
            response = await retry_transient_errors(
                client.stub.FunctionGetOutputs,
                request,
                max_retries=20,
                attempt_timeout=OUTPUTS_TIMEOUT + ATTEMPT_TIMEOUT_GRACE_PERIOD,
            )

            if len(response.outputs) == 0:
                continue

            last_entry_id = response.last_entry_id
            for item in response.outputs:
                pending_outputs.setdefault(item.input_id, 0)
                if item.input_id in completed_outputs:
                    # If this input is already completed, it means the output has already been
                    # processed and was received again due to a duplicate.
                    continue
                completed_outputs.add(item.input_id)
                num_outputs += 1
                yield item

    async def get_all_outputs_and_clean_up():
        assert client.stub
        try:
            async for item in get_all_outputs():
                yield item
        finally:
            # "ack" that we have all outputs we are interested in and let backend clear results
            request = api_pb2.FunctionGetOutputsRequest(
                function_call_id=function_call_id,
                timeout=0,
                last_entry_id="0-0",
                clear_on_success=True,
            )
            await retry_transient_errors(client.stub.FunctionGetOutputs, request)

    async def fetch_output(item: api_pb2.FunctionGetOutputsItem) -> Tuple[int, Any]:
        try:
            output = await _process_result(item.result, item.data_format, client.stub, client)
        except Exception as e:
            if return_exceptions:
                output = e
            else:
                raise e
        return (item.idx, output)

    async def poll_outputs():
        outputs = stream.iterate(get_all_outputs_and_clean_up())
        outputs_fetched = outputs | pipe.map(fetch_output, ordered=True, task_limit=BLOB_MAX_PARALLELISM)  # type: ignore

        # map to store out-of-order outputs received
        received_outputs = {}
        output_idx = 0

        async with outputs_fetched.stream() as streamer:
            async for idx, output in streamer:
                count_update()
                if not order_outputs:
                    yield _OutputValue(output)
                else:
                    # hold on to outputs for function maps, so we can reorder them correctly.
                    received_outputs[idx] = output
                    while output_idx in received_outputs:
                        output = received_outputs.pop(output_idx)
                        yield _OutputValue(output)
                        output_idx += 1

        assert len(received_outputs) == 0

    response_gen = stream.merge(drain_input_generator(), pump_inputs(), poll_outputs())

    async with response_gen.stream() as streamer:
        async for response in streamer:
            if response is not None:
                yield response.value


# Wrapper type for api_pb2.FunctionStats
@dataclass(frozen=True)
class FunctionStats:
    """Simple data structure storing stats for a running function."""

    backlog: int
    num_active_runners: int
    num_total_runners: int


def _parse_retries(
    retries: Optional[Union[int, Retries]],
    raw_f: Optional[Callable] = None,
) -> Optional[api_pb2.FunctionRetryPolicy]:
    if isinstance(retries, int):
        return Retries(
            max_retries=retries,
            initial_delay=1.0,
            backoff_coefficient=1.0,
        )._to_proto()
    elif isinstance(retries, Retries):
        return retries._to_proto()
    elif retries is None:
        return None
    else:
        err_object = f"Function {raw_f}" if raw_f else "Function"
        raise InvalidError(
            f"{err_object} retries must be an integer or instance of modal.Retries. Found: {type(retries)}"
        )


@dataclass
class _FunctionSpec:
    """
    Stores information about a Function specification.
    This is used for `modal shell` to support running shells with
    the same configuration as a user-defined Function.
    """

    image: Optional[_Image]
    mounts: Sequence[_Mount]
    secrets: Sequence[_Secret]
    network_file_systems: Dict[Union[str, PurePosixPath], _NetworkFileSystem]
    volumes: Dict[Union[str, PurePosixPath], Union[_Volume, _CloudBucketMount]]
    gpu: GPU_T
    cloud: Optional[str]
    cpu: Optional[float]
    memory: Optional[Union[int, Tuple[int, int]]]


class _Function(_Object, type_prefix="fu"):
    """Functions are the basic units of serverless execution on Modal.

    Generally, you will not construct a `Function` directly. Instead, use the
    `@app.function()` decorator on the `App` object (formerly called "Stub")
    for your application.
    """

    # TODO: more type annotations
    _info: Optional[FunctionInfo]
    _all_mounts: Collection[_Mount]
    _app: "modal.app._App"
    _obj: Any
    _web_url: Optional[str]
    _is_remote_cls_method: bool = False  # TODO(erikbern): deprecated
    _function_name: Optional[str]
    _is_method: bool
    _spec: _FunctionSpec
    _tag: str
    _raw_f: Callable[..., Any]
    _build_args: dict
    _parent: "_Function"

    @staticmethod
    def from_args(
        info: FunctionInfo,
        app,
        image: _Image,
        secret: Optional[_Secret] = None,
        secrets: Sequence[_Secret] = (),
        schedule: Optional[Schedule] = None,
        is_generator=False,
        gpu: GPU_T = None,
        # TODO: maybe break this out into a separate decorator for notebooks.
        mounts: Collection[_Mount] = (),
        network_file_systems: Dict[Union[str, PurePosixPath], _NetworkFileSystem] = {},
        allow_cross_region_volumes: bool = False,
        volumes: Dict[Union[str, PurePosixPath], Union[_Volume, _CloudBucketMount]] = {},
        webhook_config: Optional[api_pb2.WebhookConfig] = None,
        memory: Optional[Union[int, Tuple[int, int]]] = None,
        proxy: Optional[_Proxy] = None,
        retries: Optional[Union[int, Retries]] = None,
        timeout: Optional[int] = None,
        concurrency_limit: Optional[int] = None,
        allow_concurrent_inputs: Optional[int] = None,
        container_idle_timeout: Optional[int] = None,
        cpu: Optional[float] = None,
        keep_warm: Optional[int] = None,  # keep_warm=True is equivalent to keep_warm=1
        cloud: Optional[str] = None,
        _experimental_boost: bool = False,
        _experimental_scheduler: bool = False,
        _experimental_scheduler_placement: Optional[SchedulerPlacement] = None,
        is_builder_function: bool = False,
        is_auto_snapshot: bool = False,
        enable_memory_snapshot: bool = False,
        checkpointing_enabled: Optional[bool] = None,
        allow_background_volume_commits: bool = False,
        block_network: bool = False,
        max_inputs: Optional[int] = None,
    ) -> None:
        """mdmd:hidden"""
        tag = info.get_tag()

        raw_f = info.raw_f
        assert callable(raw_f)
        if schedule is not None:
            if not info.is_nullary():
                raise InvalidError(
                    f"Function {raw_f} has a schedule, so it needs to support being called with no arguments"
                )

        if secret is not None:
            deprecation_warning(
                (2024, 1, 31),
                "The singular `secret` parameter is deprecated. Pass a list to `secrets` instead.",
            )
            secrets = [secret, *secrets]

        if checkpointing_enabled is not None:
            deprecation_warning(
                (2024, 3, 4),
                "The argument `checkpointing_enabled` is now deprecated. Use `enable_memory_snapshot` instead.",
            )
            enable_memory_snapshot = checkpointing_enabled

        explicit_mounts = mounts

        if is_local():
            entrypoint_mounts = info.get_entrypoint_mount()
            all_mounts = [
                _get_client_mount(),
                *explicit_mounts,
                *entrypoint_mounts,
            ]

            if config.get("automount"):
                automounts = info.get_auto_mounts()
                all_mounts += automounts
        else:
            # skip any mount introspection/logic inside containers, since the function
            # should already be hydrated
            # TODO: maybe the entire constructor should be exited early if not local?
            all_mounts = []

        retry_policy = _parse_retries(retries, raw_f)

        gpu_config = parse_gpu_config(gpu)

        if proxy:
            # HACK: remove this once we stop using ssh tunnels for this.
            if image:
                image = image.apt_install("autossh")

        function_spec = _FunctionSpec(
            mounts=all_mounts,
            secrets=secrets,
            gpu=gpu,
            network_file_systems=network_file_systems,
            volumes=volumes,
            image=image,
            cloud=cloud,
            cpu=cpu,
            memory=memory,
        )

        if info.cls and not is_auto_snapshot:
            # Needed to avoid circular imports
            from .partial_function import _find_callables_for_cls, _PartialFunctionFlags

            build_functions = list(_find_callables_for_cls(info.cls, _PartialFunctionFlags.BUILD).values())
            for build_function in build_functions:
                snapshot_info = FunctionInfo(build_function, cls=info.cls)
                snapshot_function = _Function.from_args(
                    snapshot_info,
                    app=None,
                    image=image,
                    secrets=secrets,
                    gpu=gpu,
                    mounts=mounts,
                    network_file_systems=network_file_systems,
                    volumes=volumes,
                    memory=memory,
                    timeout=86400,  # TODO: make this an argument to `@build()`
                    cpu=cpu,
                    is_builder_function=True,
                    is_auto_snapshot=True,
                    _experimental_scheduler_placement=_experimental_scheduler_placement,
                )
                image = _Image._from_args(
                    base_images={"base": image},
                    build_function=snapshot_function,
                    force_build=image.force_build,
                )

        if keep_warm is not None and not isinstance(keep_warm, int):
            raise TypeError(f"`keep_warm` must be an int or bool, not {type(keep_warm).__name__}")

        if (keep_warm is not None) and (concurrency_limit is not None) and concurrency_limit < keep_warm:
            raise InvalidError(
                f"Function `{info.function_name}` has `{concurrency_limit=}`, strictly less than its `{keep_warm=}` parameter."
            )

        if not cloud and not is_builder_function:
            cloud = config.get("default_cloud")
        if cloud:
            cloud_provider = parse_cloud_provider(cloud)
        else:
            cloud_provider = None

        if is_generator and webhook_config:
            if webhook_config.type == api_pb2.WEBHOOK_TYPE_FUNCTION:
                raise InvalidError(
                    """Webhooks cannot be generators. If you want a streaming response, see https://modal.com/docs/guide/streaming-endpoints
                    """
                )
            else:
                raise InvalidError("Webhooks cannot be generators")

        # Validate volumes
        validated_volumes = validate_volumes(volumes)
        cloud_bucket_mounts = [(k, v) for k, v in validated_volumes if isinstance(v, _CloudBucketMount)]
        validated_volumes = [(k, v) for k, v in validated_volumes if isinstance(v, _Volume)]

        # Validate NFS
        if not isinstance(network_file_systems, dict):
            raise InvalidError("network_file_systems must be a dict[str, NetworkFileSystem] where the keys are paths")
        validated_network_file_systems = validate_mount_points("Network file system", network_file_systems)

        # Validate image
        if image is not None and not isinstance(image, _Image):
            raise InvalidError(f"Expected modal.Image object. Got {type(image)}.")

        def _deps(only_explicit_mounts=False) -> List[_Object]:
            deps: List[_Object] = list(secrets)
            if only_explicit_mounts:
                # TODO: this is a bit hacky, but all_mounts may differ in the container vs locally
                # We don't want the function dependencies to change, so we have this way to force it to
                # only include its declared dependencies.
                # Only objects that need interaction within a user's container actually need to be
                # included when only_explicit_mounts=True, so omitting auto mounts here
                # wouldn't be a problem as long as Mounts are "passive" and only loaded by the
                # worker runtime
                deps += list(explicit_mounts)
            else:
                deps += list(all_mounts)
            if proxy:
                deps.append(proxy)
            if image:
                deps.append(image)
            for _, nfs in validated_network_file_systems:
                deps.append(nfs)
            for _, vol in validated_volumes:
                deps.append(vol)
            for _, cloud_bucket_mount in cloud_bucket_mounts:
                if cloud_bucket_mount.secret:
                    deps.append(cloud_bucket_mount.secret)

            # Add implicit dependencies from the function's code
            objs: list[Object] = get_referred_objects(info.raw_f)
            _objs: list[_Object] = synchronizer._translate_in(objs)  # type: ignore
            deps += _objs
            return deps

        async def _preload(self: _Function, resolver: Resolver, existing_object_id: Optional[str]):
            assert resolver.client and resolver.client.stub
            if is_generator:
                function_type = api_pb2.Function.FUNCTION_TYPE_GENERATOR
            else:
                function_type = api_pb2.Function.FUNCTION_TYPE_FUNCTION

            req = api_pb2.FunctionPrecreateRequest(
                app_id=resolver.app_id,
                function_name=info.function_name,
                function_type=function_type,
                webhook_config=webhook_config,
                existing_function_id=existing_object_id or "",
            )
            response = await retry_transient_errors(resolver.client.stub.FunctionPrecreate, req)
            self._hydrate(response.function_id, resolver.client, response.handle_metadata)

        async def _load(self: _Function, resolver: Resolver, existing_object_id: Optional[str]):
            assert resolver.client and resolver.client.stub
            status_row = resolver.add_status_row()
            status_row.message(f"Creating {tag}...")

            if is_generator:
                function_type = api_pb2.Function.FUNCTION_TYPE_GENERATOR
            else:
                function_type = api_pb2.Function.FUNCTION_TYPE_FUNCTION

            timeout_secs = timeout

            if app and app.is_interactive and not is_builder_function:
                pty_info = get_pty_info(shell=False)
            else:
                pty_info = None

            if info.is_serialized():
                # Use cloudpickle. Used when working w/ Jupyter notebooks.
                # serialize at _load time, not function decoration time
                # otherwise we can't capture a surrounding class for lifetime methods etc.
                function_serialized = info.serialized_function()
                class_serialized = serialize(info.cls) if info.cls is not None else None

                # Ensure that large data in global variables does not blow up the gRPC payload,
                # which has maximum size 100 MiB. We set the limit lower for performance reasons.
                if len(function_serialized) > 16 << 20:  # 16 MiB
                    raise InvalidError(
                        f"Function {info.raw_f} has size {len(function_serialized)} bytes when packaged. "
                        "This is larger than the maximum limit of 16 MiB. "
                        "Try reducing the size of the closure by using parameters or mounts, not large global variables."
                    )
                elif len(function_serialized) > 256 << 10:  # 256 KiB
                    warnings.warn(
                        f"Function {info.raw_f} has size {len(function_serialized)} bytes when packaged. "
                        "This is larger than the recommended limit of 256 KiB. "
                        "Try reducing the size of the closure by using parameters or mounts, not large global variables."
                    )
            else:
                function_serialized = None
                class_serialized = None

            stub_name = ""
            if app and app.name:
                stub_name = app.name

            # Relies on dicts being ordered (true as of Python 3.6).
            volume_mounts = [
                api_pb2.VolumeMount(
                    mount_path=path,
                    volume_id=volume.object_id,
                    allow_background_commits=allow_background_volume_commits,
                )
                for path, volume in validated_volumes
            ]
            loaded_mount_ids = {m.object_id for m in all_mounts}

            # Get object dependencies
            object_dependencies = []
            for dep in _deps(only_explicit_mounts=True):
                if not dep.object_id:
                    raise Exception(f"Dependency {dep} isn't hydrated")
                object_dependencies.append(api_pb2.ObjectDependency(object_id=dep.object_id))

            # Create function remotely
            function_definition = api_pb2.Function(
                module_name=info.module_name or "",
                function_name=info.function_name,
                mount_ids=loaded_mount_ids,
                secret_ids=[secret.object_id for secret in secrets],
                image_id=(image.object_id if image else ""),
                definition_type=info.definition_type,
                function_serialized=function_serialized or b"",
                class_serialized=class_serialized or b"",
                function_type=function_type,
                resources=convert_fn_config_to_resources_config(cpu=cpu, memory=memory, gpu=gpu),
                webhook_config=webhook_config,
                shared_volume_mounts=network_file_system_mount_protos(
                    validated_network_file_systems, allow_cross_region_volumes
                ),
                volume_mounts=volume_mounts,
                proxy_id=(proxy.object_id if proxy else None),
                retry_policy=retry_policy,
                timeout_secs=timeout_secs or 0,
                task_idle_timeout_secs=container_idle_timeout or 0,
                concurrency_limit=concurrency_limit or 0,
                pty_info=pty_info,
                cloud_provider=cloud_provider,
                warm_pool_size=keep_warm or 0,
                runtime=config.get("function_runtime"),
                runtime_debug=config.get("function_runtime_debug"),
                stub_name=stub_name,
                is_builder_function=is_builder_function,
                allow_concurrent_inputs=allow_concurrent_inputs or 0,
                worker_id=config.get("worker_id"),
                is_auto_snapshot=is_auto_snapshot,
                is_method=bool(info.cls),
                checkpointing_enabled=enable_memory_snapshot,
                is_checkpointing_function=False,
                object_dependencies=object_dependencies,
                block_network=block_network,
                max_inputs=max_inputs or 0,
                cloud_bucket_mounts=cloud_bucket_mounts_to_proto(cloud_bucket_mounts),
                _experimental_boost=_experimental_boost,
                _experimental_scheduler=_experimental_scheduler,
                _experimental_scheduler_placement=_experimental_scheduler_placement.proto
                if _experimental_scheduler_placement
                else None,
            )
            request = api_pb2.FunctionCreateRequest(
                app_id=resolver.app_id,
                function=function_definition,
                schedule=schedule.proto_message if schedule is not None else None,
                existing_function_id=existing_object_id or "",
            )
            try:
                response: api_pb2.FunctionCreateResponse = await retry_transient_errors(
                    resolver.client.stub.FunctionCreate, request
                )
            except GRPCError as exc:
                if exc.status == Status.INVALID_ARGUMENT:
                    raise InvalidError(exc.message)
                if exc.status == Status.FAILED_PRECONDITION:
                    raise InvalidError(exc.message)
                if exc.message and "Received :status = '413'" in exc.message:
                    raise InvalidError(f"Function {raw_f} is too large to deploy.")
                raise

            if response.function.web_url:
                # Ensure terms used here match terms used in modal.com/docs/guide/webhook-urls doc.
                if response.function.web_url_info.truncated:
                    suffix = " [grey70](label truncated)[/grey70]"
                elif response.function.web_url_info.has_unique_hash:
                    suffix = " [grey70](label includes conflict-avoidance hash)[/grey70]"
                elif response.function.web_url_info.label_stolen:
                    suffix = " [grey70](label stolen)[/grey70]"
                else:
                    suffix = ""
                # TODO: this is only printed when we're showing progress. Maybe move this somewhere else.
                status_row.finish(f"Created {tag} => [magenta underline]{response.web_url}[/magenta underline]{suffix}")

                # Print custom domain in terminal
                for custom_domain in response.function.custom_domain_info:
                    custom_domain_status_row = resolver.add_status_row()
                    custom_domain_status_row.finish(
                        f"Custom domain for {tag} => [magenta underline]{custom_domain.url}[/magenta underline]{suffix}"
                    )

            else:
                status_row.finish(f"Created {tag}.")

            self._hydrate(response.function_id, resolver.client, response.handle_metadata)

        rep = f"Function({tag})"
        obj = _Function._from_loader(_load, rep, preload=_preload, deps=_deps)

        obj._raw_f = raw_f
        obj._info = info
        obj._tag = tag
        obj._all_mounts = all_mounts  # needed for modal.serve file watching
        obj._app = app  # needed for CLI right now
        obj._obj = None
        obj._is_generator = is_generator
        obj._is_method = bool(info.cls)
        obj._spec = function_spec  # needed for modal shell

        # Used to check whether we should rebuild an image using run_function
        # Plaintext source and arg definition for the function, so it's part of the image
        # hash. We can't use the cloudpickle hash because it's not very stable.
        obj._build_args = dict(  # See get_build_def
            secrets=repr(secrets),
            gpu_config=repr(gpu_config),
            mounts=repr(mounts),
            network_file_systems=repr(network_file_systems),
        )

        return obj

    def from_parametrized(
        self,
        obj,
        from_other_workspace: bool,
        options: Optional[api_pb2.FunctionOptions],
        args: Sized,
        kwargs: Dict[str, Any],
    ) -> "_Function":
        """mdmd:hidden"""

        async def _load(self: _Function, resolver: Resolver, existing_object_id: Optional[str]):
            if not self._parent.is_hydrated:
                raise ExecutionError(
                    "Base function in class has not been hydrated. This might happen if an object is"
                    " defined on a different stub, or if it's on the same stub but it didn't get"
                    " created because it wasn't defined in global scope."
                )
            assert self._parent._client.stub
            serialized_params = serialize((args, kwargs))
            environment_name = _get_environment_name(None, resolver)
            req = api_pb2.FunctionBindParamsRequest(
                function_id=self._parent._object_id,
                serialized_params=serialized_params,
                function_options=options,
                environment_name=environment_name
                or "",  # TODO: investigate shouldn't environment name always be specified here?
            )
            response = await retry_transient_errors(self._parent._client.stub.FunctionBindParams, req)
            self._hydrate(response.bound_function_id, self._parent._client, response.handle_metadata)

        fun = _Function._from_loader(_load, "Function(parametrized)", hydrate_lazily=True)
        if len(args) + len(kwargs) == 0 and not from_other_workspace and options is None and self.is_hydrated:
            # Edge case that lets us hydrate all objects right away
            fun._hydrate_from_other(self)
        fun._is_remote_cls_method = True  # TODO(erikbern): deprecated
        fun._info = self._info
        fun._obj = obj
        fun._is_generator = self._is_generator
        fun._is_method = True
        fun._parent = self

        return fun

    @live_method
    async def keep_warm(self, warm_pool_size: int) -> None:
        """Set the warm pool size for the function (including parametrized functions).

        Please exercise care when using this advanced feature! Setting and forgetting a warm pool on functions can lead to increased costs.

        ```python
        # Usage on a regular function.
        f = modal.Function.lookup("my-app", "function")
        f.keep_warm(2)

        # Usage on a parametrized function.
        Model = modal.Cls.lookup("my-app", "Model")
        Model("fine-tuned-model").inference.keep_warm(2)
        ```
        """

        assert self._client and self._client.stub
        request = api_pb2.FunctionUpdateSchedulingParamsRequest(
            function_id=self._object_id, warm_pool_size_override=warm_pool_size
        )
        await retry_transient_errors(self._client.stub.FunctionUpdateSchedulingParams, request)

    @classmethod
    def from_name(
        cls: Type["_Function"],
        app_name: str,
        tag: Optional[str] = None,
        namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
        environment_name: Optional[str] = None,
    ) -> "_Function":
        """Retrieve a function with a given name and tag.

        ```python
        other_function = modal.Function.from_name("other-app", "function")
        ```
        """

        async def _load_remote(self: _Function, resolver: Resolver, existing_object_id: Optional[str]):
            assert resolver.client and resolver.client.stub
            request = api_pb2.FunctionGetRequest(
                app_name=app_name,
                object_tag=tag or "",
                namespace=namespace,
                environment_name=_get_environment_name(environment_name, resolver) or "",
            )
            try:
                response = await retry_transient_errors(resolver.client.stub.FunctionGet, request)
            except GRPCError as exc:
                if exc.status == Status.NOT_FOUND:
                    raise NotFoundError(exc.message)
                else:
                    raise

            self._hydrate(response.function_id, resolver.client, response.handle_metadata)

        rep = f"Ref({app_name})"
        return cls._from_loader(_load_remote, rep, is_another_app=True)

    @staticmethod
    async def lookup(
        app_name: str,
        tag: Optional[str] = None,
        namespace=api_pb2.DEPLOYMENT_NAMESPACE_WORKSPACE,
        client: Optional[_Client] = None,
        environment_name: Optional[str] = None,
    ) -> "_Function":
        """Lookup a function with a given name and tag.

        ```python
        other_function = modal.Function.lookup("other-app", "function")
        ```
        """
        obj = _Function.from_name(app_name, tag, namespace=namespace, environment_name=environment_name)
        if client is None:
            client = await _Client.from_env()
        resolver = Resolver(client=client)
        await resolver.load(obj)
        return obj

    @property
    def tag(self) -> str:
        """mdmd:hidden"""
        assert self._tag
        return self._tag

    @property
    def app(self) -> "modal.app._App":
        """mdmd:hidden"""
        return self._app

    @property
    def stub(self) -> "modal.app._App":
        """mdmd:hidden"""
        # Deprecated soon, only for backwards compatibility
        return self._app

    @property
    def info(self) -> FunctionInfo:
        """mdmd:hidden"""
        assert self._info
        return self._info

    @property
    def spec(self) -> _FunctionSpec:
        """mdmd:hidden"""
        return self._spec

    def get_build_def(self) -> str:
        """mdmd:hidden"""
        assert hasattr(self, "_raw_f") and hasattr(self, "_build_args")
        return f"{inspect.getsource(self._raw_f)}\n{repr(self._build_args)}"

    # Live handle methods

    def _initialize_from_empty(self):
        # Overridden concrete implementation of base class method
        self._progress = None
        self._is_generator = None
        self._web_url = None
        self._output_mgr: Optional[OutputManager] = None
        self._mute_cancellation = (
            False  # set when a user terminates the app intentionally, to prevent useless traceback spam
        )
        self._function_name = None
        self._info = None

    def _hydrate_metadata(self, metadata: Optional[Message]):
        # Overridden concrete implementation of base class method
        assert metadata and isinstance(metadata, (api_pb2.Function, api_pb2.FunctionHandleMetadata))
        self._is_generator = metadata.function_type == api_pb2.Function.FUNCTION_TYPE_GENERATOR
        self._web_url = metadata.web_url
        self._function_name = metadata.function_name
        self._is_method = metadata.is_method

    def _get_metadata(self):
        # Overridden concrete implementation of base class method
        assert self._function_name
        return api_pb2.FunctionHandleMetadata(
            function_name=self._function_name,
            function_type=(
                api_pb2.Function.FUNCTION_TYPE_GENERATOR
                if self._is_generator
                else api_pb2.Function.FUNCTION_TYPE_FUNCTION
            ),
            web_url=self._web_url or "",
        )

    def _set_mute_cancellation(self, value: bool = True):
        self._mute_cancellation = value

    def _set_output_mgr(self, output_mgr: OutputManager):
        self._output_mgr = output_mgr

    @property
    def web_url(self) -> str:
        """URL of a Function running as a web endpoint."""
        if not self._web_url:
            raise ValueError(
                f"No web_url can be found for function {self._function_name}. web_url can only be referenced from a running app context"
            )
        return self._web_url

    @property
    def is_generator(self) -> bool:
        """mdmd:hidden"""
        assert self._is_generator is not None
        return self._is_generator

    @live_method_gen
    async def _map(
        self, input_queue: _SynchronizedQueue, order_outputs: bool, return_exceptions: bool
    ) -> AsyncGenerator[Any, None]:
        """mdmd:hidden

        Synchronicity-wrapped map implementation. To be safe against invocations of user code in the synchronicity thread
        it doesn't accept an [async]iterator, and instead takes a _SynchronizedQueue instance.

        _SynchronizedQueue is used instead of asyncio.Queue so that the main thread can put
        items in the queue safely.
        """
        if self._web_url:
            raise InvalidError(
                "A web endpoint function cannot be directly invoked for parallel remote execution. "
                f"Invoke this function via its web url '{self._web_url}' or call it locally: {self._function_name}()."
            )
        if self._is_generator:
            raise InvalidError("A generator function cannot be called with `.map(...)`.")

        assert self._function_name
        count_update_callback = (
            self._output_mgr.function_progress_callback(self._function_name, total=None) if self._output_mgr else None
        )

        async for item in _map_invocation(
            self.object_id,
            input_queue,
            self._client,
            order_outputs,
            return_exceptions,
            count_update_callback,
        ):
            yield item

    async def _call_function(self, args, kwargs):
        invocation = await _Invocation.create(self.object_id, args, kwargs, self._client)
        try:
            return await invocation.run_function()
        except asyncio.CancelledError:
            # this can happen if the user terminates a program, triggering a cancellation cascade
            if not self._mute_cancellation:
                raise

    async def _call_function_nowait(self, args, kwargs) -> _Invocation:
        return await _Invocation.create(self.object_id, args, kwargs, self._client)

    @warn_if_generator_is_not_consumed()
    @live_method_gen
    @synchronizer.no_input_translation
    async def _call_generator(self, args, kwargs):
        invocation = await _Invocation.create(self.object_id, args, kwargs, self._client)
        async for res in invocation.run_generator():
            yield res

    @synchronizer.no_io_translation
    async def _call_generator_nowait(self, args, kwargs):
        return await _Invocation.create(self.object_id, args, kwargs, self._client)

    # note that `map()` is not synchronicity-wrapped, since it accepts executable code in the form of
    # iterators that we don't want to run inside the synchronicity thread. We delegate to `._map()` with
    # a safer Queue as input
    @synchronizer.nowrap
    @warn_if_generator_is_not_consumed(function_name="Function.map")
    def _map_sync(
        self,
        *input_iterators: Iterable[Any],  # one input iterator per argument in the mapped-over function/generator
        kwargs={},  # any extra keyword arguments for the function
        order_outputs: bool = True,  # return outputs in order
        return_exceptions: bool = False,  # propagate exceptions (False) or aggregate them in the results list (True)
    ) -> AsyncOrSyncIteratable:
        """Parallel map over a set of inputs.

        Takes one iterator argument per argument in the function being mapped over.

        Example:
        ```python
        @stub.function()
        def my_func(a):
            return a ** 2


        @stub.local_entrypoint()
        def main():
            assert list(my_func.map([1, 2, 3, 4])) == [1, 4, 9, 16]
        ```

        If applied to a `stub.function`, `map()` returns one result per input and the output order
        is guaranteed to be the same as the input order. Set `order_outputs=False` to return results
        in the order that they are completed instead.

        `return_exceptions` can be used to treat exceptions as successful results:

        ```python
        @stub.function()
        def my_func(a):
            if a == 2:
                raise Exception("ohno")
            return a ** 2


        @stub.local_entrypoint()
        def main():
            # [0, 1, UserCodeException(Exception('ohno'))]
            print(list(my_func.map(range(3), return_exceptions=True)))
        ```
        """

        return AsyncOrSyncIteratable(
            self._map_async(
                *input_iterators, kwargs=kwargs, order_outputs=order_outputs, return_exceptions=return_exceptions
            ),
            nested_async_message="You can't iter(Function.map()) or Function.for_each() from an async function. Use async for ... Function.map.aio() or Function.for_each.aio() instead.",
        )

    @synchronizer.nowrap
    @warn_if_generator_is_not_consumed(function_name="Function.map.aio")
    async def _map_async(
        self,
        *input_iterators: Union[
            Iterable[Any], AsyncIterable[Any]
        ],  # one input iterator per argument in the mapped-over function/generator
        kwargs={},  # any extra keyword arguments for the function
        order_outputs: bool = True,  # return outputs in order
        return_exceptions: bool = False,  # propagate exceptions (False) or aggregate them in the results list (True)
    ) -> AsyncGenerator[Any, None]:
        """mdmd:hidden
        This runs in an event loop on the main thread

        It concurrently feeds new input to the input queue and yields available outputs
        to the caller.
        Note that since the iterator(s) can block, it's a bit opaque how often the event
        loop decides to get a new input vs how often it will emit a new output.
        We could make this explicit as an improvement or even let users decide what they
        prefer: throughput (prioritize queueing inputs) or latency (prioritize yielding results)
        """
        raw_input_queue: Any = SynchronizedQueue()  # type: ignore
        raw_input_queue.init()

        async def feed_queue():
            # This runs in a main thread event loop, so it doesn't block the synchronizer loop
            async with stream.zip(*[stream.iterate(it) for it in input_iterators]).stream() as streamer:
                async for args in streamer:
                    await raw_input_queue.put.aio((args, kwargs))
            await raw_input_queue.put.aio(None)  # end-of-input sentinel

        feed_input_task = asyncio.create_task(feed_queue())

        try:
            async for output in self._map.aio(raw_input_queue, order_outputs, return_exceptions):  # type: ignore[reportFunctionMemberAccess]
                yield output
        finally:
            feed_input_task.cancel()  # should only be needed in case of exceptions

    def _for_each_sync(self, *input_iterators, kwargs={}, ignore_exceptions: bool = False):
        """Execute function for all inputs, ignoring outputs.

        Convenient alias for `.map()` in cases where the function just needs to be called.
        as the caller doesn't have to consume the generator to process the inputs.
        """
        # TODO(erikbern): it would be better if this is more like a map_spawn that immediately exits
        # rather than iterating over the result
        for _ in self.map(*input_iterators, kwargs=kwargs, order_outputs=False, return_exceptions=ignore_exceptions):
            pass

    @synchronizer.nowrap
    async def _for_each_async(self, *input_iterators, kwargs={}, ignore_exceptions: bool = False):
        async for _ in self.map.aio(  # type: ignore
            *input_iterators, kwargs=kwargs, order_outputs=False, return_exceptions=ignore_exceptions
        ):
            pass

    @synchronizer.nowrap
    @warn_if_generator_is_not_consumed(function_name="Function.starmap")
    async def _starmap_async(
        self,
        input_iterator: Union[Iterable[Sequence[Any]], AsyncIterable[Sequence[Any]]],
        kwargs={},
        order_outputs: bool = True,
        return_exceptions: bool = False,
    ) -> typing.AsyncIterable[Any]:
        raw_input_queue: Any = SynchronizedQueue()  # type: ignore
        raw_input_queue.init()

        async def feed_queue():
            # This runs in a main thread event loop, so it doesn't block the synchronizer loop
            async with stream.iterate(input_iterator).stream() as streamer:
                async for args in streamer:
                    await raw_input_queue.put.aio((args, kwargs))
            await raw_input_queue.put.aio(None)  # end-of-input sentinel

        feed_input_task = asyncio.create_task(feed_queue())
        try:
            async for output in self._map.aio(raw_input_queue, order_outputs, return_exceptions):  # type: ignore[reportFunctionMemberAccess]
                yield output
        finally:
            feed_input_task.cancel()  # should only be needed in case of exceptions

    @synchronizer.nowrap
    @warn_if_generator_is_not_consumed(function_name="Function.starmap.aio")
    def _starmap_sync(
        self,
        input_iterator: Iterable[Sequence[Any]],
        kwargs={},
        order_outputs: bool = True,
        return_exceptions: bool = False,
    ) -> AsyncOrSyncIteratable:
        """Like `map`, but spreads arguments over multiple function arguments.

        Assumes every input is a sequence (e.g. a tuple).

        Example:
        ```python
        @stub.function()
        def my_func(a, b):
            return a + b


        @stub.local_entrypoint()
        def main():
            assert list(my_func.starmap([(1, 2), (3, 4)])) == [3, 7]
        ```
        """
        return AsyncOrSyncIteratable(
            self._starmap_async(
                input_iterator, kwargs=kwargs, order_outputs=order_outputs, return_exceptions=return_exceptions
            ),
            nested_async_message="You can't run Function.map() or Function.for_each() from an async function. Use Function.map.aio()/Function.for_each.aio() instead.",
        )

    @synchronizer.no_io_translation
    @live_method
    async def remote(self, *args, **kwargs) -> Any:
        """
        Calls the function remotely, executing it with the given arguments and returning the execution's result.
        """
        # TODO: Generics/TypeVars
        if self._web_url:
            raise InvalidError(
                "A web endpoint function cannot be invoked for remote execution with `.remote`. "
                f"Invoke this function via its web url '{self._web_url}' or call it locally: {self._function_name}()."
            )
        if self._is_generator:
            raise InvalidError(
                "A generator function cannot be called with `.remote(...)`. Use `.remote_gen(...)` instead."
            )

        return await self._call_function(args, kwargs)

    @synchronizer.no_io_translation
    @live_method_gen
    async def remote_gen(self, *args, **kwargs) -> AsyncGenerator[Any, None]:
        """
        Calls the generator remotely, executing it with the given arguments and returning the execution's result.
        """
        # TODO: Generics/TypeVars
        if self._web_url:
            raise InvalidError(
                "A web endpoint function cannot be invoked for remote execution with `.remote`. "
                f"Invoke this function via its web url '{self._web_url}' or call it locally: {self._function_name}()."
            )

        if not self._is_generator:
            raise InvalidError(
                "A non-generator function cannot be called with `.remote_gen(...)`. Use `.remote(...)` instead."
            )
        async for item in self._call_generator(args, kwargs):  # type: ignore
            yield item

    @synchronizer.no_io_translation
    @live_method
    async def shell(self, *args, **kwargs) -> None:
        if self._is_generator:
            async for item in self._call_generator(args, kwargs):
                pass
        else:
            await self._call_function(args, kwargs)

    def _get_is_remote_cls_method(self):
        return self._is_remote_cls_method

    def _get_info(self):
        return self._info

    def _get_obj(self):
        if not self._is_method:
            return None
        elif not self._obj:
            raise ExecutionError("Method has no local object")
        else:
            return self._obj

    @synchronizer.nowrap
    def local(self, *args, **kwargs) -> Any:
        """
        Calls the function locally, executing it with the given arguments and returning the execution's result.

        The function will execute in the same environment as the caller, just like calling the underlying function
        directly in Python. In particular, secrets will not be available through environment variables.
        """
        # TODO(erikbern): it would be nice to remove the nowrap thing, but right now that would cause
        # "user code" to run on the synchronicity thread, which seems bad
        info = self._get_info()
        if not info:
            msg = (
                "The definition for this function is missing so it is not possible to invoke it locally. "
                "If this function was retrieved via `Function.lookup` you need to use `.remote()`."
            )
            raise ExecutionError(msg)

        obj = self._get_obj()

        if not obj:
            fun = info.raw_f
            return fun(*args, **kwargs)
        else:
            # This is a method on a class, so bind the self to the function
            local_obj = obj.get_local_obj()
            fun = info.raw_f.__get__(local_obj)

            if is_async(info.raw_f):
                # We want to run __aenter__ and fun in the same coroutine
                async def coro():
                    await obj.aenter()
                    return await fun(*args, **kwargs)

                return coro()
            else:
                obj.enter()
                return fun(*args, **kwargs)

    @synchronizer.no_input_translation
    @live_method
    async def spawn(self, *args, **kwargs) -> Optional["_FunctionCall"]:
        """Calls the function with the given arguments, without waiting for the results.

        Returns a `modal.functions.FunctionCall` object, that can later be polled or waited for using `.get(timeout=...)`.
        Conceptually similar to `multiprocessing.pool.apply_async`, or a Future/Promise in other contexts.

        *Note:* `.spawn()` on a modal generator function does call and execute the generator, but does not currently
        return a function handle for polling the result.
        """
        if self._is_generator:
            await self._call_generator_nowait(args, kwargs)
            return None

        invocation = await self._call_function_nowait(args, kwargs)
        return _FunctionCall._new_hydrated(invocation.function_call_id, invocation.client, None)

    def get_raw_f(self) -> Callable[..., Any]:
        """Return the inner Python object wrapped by this Modal Function."""
        if not self._info:
            raise AttributeError("_info has not been set on this FunctionHandle and not available in this context")

        return self._info.raw_f

    @live_method
    async def get_current_stats(self) -> FunctionStats:
        """Return a `FunctionStats` object describing the current function's queue and runner counts."""
        assert self._client.stub
        resp = await self._client.stub.FunctionGetCurrentStats(
            api_pb2.FunctionGetCurrentStatsRequest(function_id=self.object_id)
        )
        return FunctionStats(
            backlog=resp.backlog, num_active_runners=resp.num_active_tasks, num_total_runners=resp.num_total_tasks
        )

    # A bit hacky - but the map-style functions need to not be synchronicity-wrapped
    # in order to not execute their input iterators on the synchronicity event loop.
    # We still need to wrap them using MethodWithAio to maintain a synchronicity-like
    # api with `.aio` and get working type-stubs and reference docs generation:
    map = MethodWithAio(_map_sync, _map_async, synchronizer)
    starmap = MethodWithAio(_starmap_sync, _starmap_async, synchronizer)
    for_each = MethodWithAio(_for_each_sync, _for_each_async, synchronizer)


Function = synchronize_api(_Function)


class _FunctionCall(_Object, type_prefix="fc"):
    """A reference to an executed function call.

    Constructed using `.spawn(...)` on a Modal function with the same
    arguments that a function normally takes. Acts as a reference to
    an ongoing function call that can be passed around and used to
    poll or fetch function results at some later time.

    Conceptually similar to a Future/Promise/AsyncResult in other contexts and languages.
    """

    def _invocation(self):
        assert self._client.stub
        return _Invocation(self._client.stub, self.object_id, self._client)

    async def get(self, timeout: Optional[float] = None):
        """Get the result of the function call.

        This function waits indefinitely by default. It takes an optional
        `timeout` argument that specifies the maximum number of seconds to wait,
        which can be set to `0` to poll for an output immediately.

        The returned coroutine is not cancellation-safe.
        """
        return await self._invocation().poll_function(timeout=timeout)

    async def get_call_graph(self) -> List[InputInfo]:
        """Returns a structure representing the call graph from a given root
        call ID, along with the status of execution for each node.

        See [`modal.call_graph`](/docs/reference/modal.call_graph) reference page
        for documentation on the structure of the returned `InputInfo` items.
        """
        assert self._client and self._client.stub
        request = api_pb2.FunctionGetCallGraphRequest(function_call_id=self.object_id)
        response = await retry_transient_errors(self._client.stub.FunctionGetCallGraph, request)
        return _reconstruct_call_graph(response)

    async def cancel(self):
        """Cancels the function call, which will stop its execution and mark its inputs as [`TERMINATED`](/docs/reference/modal.call_graph#modalcall_graphinputstatus)."""
        request = api_pb2.FunctionCallCancelRequest(function_call_id=self.object_id)
        assert self._client and self._client.stub
        await retry_transient_errors(self._client.stub.FunctionCallCancel, request)

    @staticmethod
    async def from_id(function_call_id: str, client: Optional[_Client] = None) -> "_FunctionCall":
        if client is None:
            client = await _Client.from_env()

        return _FunctionCall._new_hydrated(function_call_id, client, None)


FunctionCall = synchronize_api(_FunctionCall)


async def _gather(*function_calls: _FunctionCall):
    """Wait until all Modal function calls have results before returning

    Accepts a variable number of FunctionCall objects as returned by `Function.spawn()`.

    Returns a list of results from each function call, or raises an exception
    of the first failing function call.

    E.g.

    ```python notest
    function_call_1 = slow_func_1.spawn()
    function_call_2 = slow_func_2.spawn()

    result_1, result_2 = gather(function_call_1, function_call_2)
    ```
    """
    try:
        return await asyncio.gather(*[fc.get() for fc in function_calls])
    except Exception as exc:
        # TODO: kill all running function calls
        raise exc


gather = synchronize_api(_gather)


_current_input_id: ContextVar = ContextVar("_current_input_id")
_current_function_call_id: ContextVar = ContextVar("_current_function_call_id")


def current_input_id() -> Optional[str]:
    """Returns the input ID for the current input.

    Can only be called from Modal function (i.e. in a container context).

    ```python
    from modal import current_input_id

    @stub.function()
    def process_stuff():
        print(f"Starting to process {current_input_id()}")
    ```
    """
    try:
        return _current_input_id.get()
    except LookupError:
        return None


def current_function_call_id() -> Optional[str]:
    """Returns the function call ID for the current input.

    Can only be called from Modal function (i.e. in a container context).

    ```python
    from modal import current_function_call_id

    @stub.function()
    def process_stuff():
        print(f"Starting to process input from {current_function_call_id()}")
    ```
    """
    try:
        return _current_function_call_id.get()
    except LookupError:
        return None


def _set_current_context_ids(input_id: str, function_call_id: str) -> Callable[[], None]:
    input_token = _current_input_id.set(input_id)
    function_call_token = _current_function_call_id.set(function_call_id)

    def _reset_current_context_ids():
        _current_input_id.reset(input_token)
        _current_function_call_id.reset(function_call_token)

    return _reset_current_context_ids
