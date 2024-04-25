#!/usr/bin/env python3

import asyncio
import dataclasses as dc
import inspect
import threading
import time
from typing import Any, Callable, Dict, List

# import app.shared.error_handler.app as error_handler
import app.shared.format_main_arguments.app as format_main_arguments

RESULTS = {}
LOCK = threading.Lock()


@dc.dataclass
class Body:
  target: Callable | str | None = None
  args: List[List[Any]] | List[Any] | None = None
  kwargs: List[Dict] | Dict | None = None
  store_name: str = "RESULTS"


@dc.dataclass
class Data:
  body: Body | None = None
  timestamp: int = dc.field(default_factory=lambda: int(time.time()))
  module_name: str | None = None
  arguments: List[dict] | None = None
  threads: List[threading.Thread] | None = None
  results: List[Any] | None = None
  call_method: str = "module"


CONVERT_VALUE = {
  # ruff: noqa: ARG005
  "NoneType": lambda value: [],
  "list": lambda value: value,
  "dict": lambda value: value,
  "*": lambda value: [value],
}


async def convert_value(value: Any) -> List[Any]:
  value_type = type(value).__name__
  if value_type not in CONVERT_VALUE:
    value_type = "*"
  function = CONVERT_VALUE[value_type]
  value = function(value=value)
  return value


async def format_target_args_and_kwargs(data: Data) -> Data:
  arguments = ["args", "kwargs"]
  store = []
  for argument in arguments:
    field = getattr(data.body, argument)

    if not field:
      continue

    for value in field:
      value_formatted = await convert_value(value=value)

      if argument == "kwargs":
        value_formatted = {argument: {argument: value_formatted}}
      elif argument == "args":
        value_formatted = {argument: [value_formatted]}
      store.append(value_formatted)
    data.arguments = store
  return data


def update_results(
  result: Any,
  target: Callable,
  timestamp: int,
) -> None:
  key = f"{target.__name__}.{timestamp}"

  global RESULTS
  if key not in RESULTS:
    RESULTS[key] = []
  RESULTS[key].append(result)


# ruff: noqa: ARG001
async def get_entrypoint_for_sync_target_with_args(
  target: Callable,
  timestamp: int,
  args: list | tuple,
  kwargs: None = None,
) -> Any:
  def entrypoint(args) -> None:
    result = None
    try:
      result = target(*args)
    except Exception as e:
      result = e
    update_results(
      result=result,
      target=target,
      timestamp=timestamp,
    )

  return entrypoint


# ruff: noqa: ARG001
async def get_entrypoint_for_sync_target_with_kwargs(
  target: Callable,
  timestamp: int,
  kwargs: dict,
  args: None = None,
) -> Any:
  def entrypoint(kwargs) -> None:
    result = None
    try:
      result = target(**kwargs)
    except Exception as e:
      result = e
    update_results(
      result=result,
      target=target,
      timestamp=timestamp,
    )

  return entrypoint


# ruff: noqa: ARG001
async def get_entrypoint_for_async_target_with_args(
  target: Callable,
  timestamp: int,
  args: list | tuple,
  kwargs: None = None,
) -> Any:
  def entrypoint(args) -> None:
    result = asyncio.gather(target(*args), return_exceptions=True)
    update_results(
      result=result,
      target=target,
      timestamp=timestamp,
    )

  return entrypoint


# ruff: noqa: ARG001await
async def get_entrypoint_for_async_target_with_kwargs(
  target: Callable,
  timestamp: int,
  kwargs: dict,
  args: None = None,
) -> Any:
  def entrypoint(kwargs):
    # result = None
    # try:
    #   result = asyncio.run(target(**kwargs))
    # except Exception as e:
    #   result = e
    result = asyncio.run(target(**kwargs), debug=True)
    # print(result)
    update_results(
      result=result,
      target=target,
      timestamp=timestamp,
    )

  return entrypoint


GET_ENTRYPOINTS = {
  "async.args": get_entrypoint_for_async_target_with_args,
  "async.kwargs": get_entrypoint_for_async_target_with_kwargs,
  "sync.args": get_entrypoint_for_sync_target_with_args,
  "sync.kwargs": get_entrypoint_for_sync_target_with_kwargs,
}


async def get_entrypoints(data: Data) -> Data:
  coroutine = inspect.iscoroutinefunction(data.body.target)
  coroutine = "sync" if not coroutine else "async"

  for argument in data.arguments:
    argument_type = next(iter(argument))
    cases = f"{coroutine}.{argument_type}"
    function = GET_ENTRYPOINTS[cases]
    argument["target"] = data.body.target
    argument["timestamp"] = data.timestamp
    argument["entrypoint"] = await function(**argument)
    del argument["target"]
  return data


async def create_thread_for_entrypoint_and_arguments(
  entrypoint: Callable,
  args=None,
  kwargs=None,
) -> threading.Thread:
  if kwargs:
    thread = threading.Thread(
      target=entrypoint,
      kwargs=kwargs,
      daemon=True,
    )
    return thread

  if args:
    thread = threading.Thread(
      target=entrypoint,
      args=args,
      daemon=True,
    )
    return thread


async def create_threads(data: Data) -> Data:
  data.threads = []
  for argument in data.arguments:
    del argument["timestamp"]
    thread = await create_thread_for_entrypoint_and_arguments(**argument)
    # Lock to prevent duplicate threads from being created
    with LOCK:
      time.sleep(0.1)
    data.threads.append(thread)
  return data


async def start_threads(data: Data) -> Data:
  """Runs threads in parallel and waits for each thread to finish before
    returning True"""
  # Run threads in parallel
  for thread in data.threads:
    thread.start()

  # Wait for each thread to terminate
  for thread in data.threads:
    thread.join()

  return data


async def get_store_from_targets_module(
  target: Callable,
  store_name: str,
) -> List[Any]:
  """Returns a global variable, from the target function's module, that's used
    to store results from executing the target in multiple threads."""
  module = inspect.getmodule(target)
  if hasattr(module, store_name) is True:
    # setattr(module, 'STORE', RESULTS)
    return getattr(module, store_name)

  return []


# ruff: noqa: ARG001
async def main(
  target: List[Callable] | Callable | None = None,
  kwargs: List[dict] | dict | None = None,
  args: List[Any] | None = None,
) -> List[Any]:
  data = await format_main_arguments.main(
    _locals=locals(),
    data_classes={"body": Body},
    main_data_class=Data,
  )
  data = await format_target_args_and_kwargs(data=data)
  data.module = inspect.getmodule(data.body.target)
  data = await get_entrypoints(data=data)
  data = await create_threads(data=data)
  await start_threads(data=data)
  return data.results


async def example() -> None:
  from app.app.operations.multithread.test_resources import app as hello_world

  args = [[None], ["Earth"]]
  kwargs = [{"name": "Mars"}, {"name": None}, {"name": "Venus"}, {"name": []}]

  global RESULTS
  RESULTS = {}
  # Synchronous target
  data = await main(
    target=hello_world.main_sync,
    args=args,
    kwargs=kwargs,
  )
  print("sync", data)

  RESULTS = {}
  # Asynchronous target
  data = await main(
    target=hello_world.main_async,
    args=args,
    kwargs=kwargs,
  )
  print("async", data)


if __name__ == '__main__':
  asyncio.run(example())
