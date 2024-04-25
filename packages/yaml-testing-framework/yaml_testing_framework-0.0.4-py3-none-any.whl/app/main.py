#!/usr/bin/env python3

import dataclasses as dc
import os
from types import ModuleType
from typing import Any, Callable, List

import yaml

from app.operations.assertions import app as assertions
from app.operations.cast import app as cast
from app.operations.get_file_paths import app as get_file_paths
from app.operations.get_function_definitions import (
  app as get_function_definitions,
)
from app.operations.multithread import app as multithread
from app.operations.patch import app as patch
from app.shared.dacite_wrapper import app as dacite_wrapper
from app.shared.format_main_arguments import app as format_main_arguments
from app.shared.get_environment import app as get_environment
from app.shared.get_module import app as get_module

MODULE_PATH = __file__
ENV = get_environment.main(module_path=MODULE_PATH)

EXCLUDE_PATTERNS = [
  '.venv',
  '.eggs',
  'build',
  '_ignore',
  'test_entrypoint.py',
  'plugin.py',
]


@dc.dataclass
class DataClass:
  ...


@dc.dataclass
class Body:
  project_path: str | None = None
  exclude_patterns: str | None = None
  text: str | None = None


@dc.dataclass
class Base:
  description: str | None = None
  cast_arguments: dict | str | None = None
  cast_result: dict | str | None = None
  patch: List[dict] | dict | None = None
  assertions: List[str | dict] | str | dict | None = None
  passed: List[bool] | None = None


@dc.dataclass
class Test(Base):
  arguments: Any | None = None
  result: Any | None = None
  exception: Exception | None = None
  module: ModuleType | None = None
  function: Callable | str | None = None


@dc.dataclass
class Function(Base):
  module: ModuleType | None = None
  name: str | None = None
  description: str | None = None
  tests: List[Test] | None = None
  results: List[Any] | None = None


@dc.dataclass
class Module:
  module: ModuleType | None = None
  function_names: List[str] | None = None
  functions: List[Function] | dict | None = None


@dc.dataclass
class Data:
  body: Body | None = None
  test_files: List[get_file_paths.FilePaths] | None = None
  modules: List[Module] | None = None
  results: Any | None = None


class Store:
  pass


async def get_test_data_from_yml(path: get_file_paths.FilePaths,) -> dict:
  test_data = {}

  if not os.path.exists(str(path.yaml)):
    return test_data

  with open(
    file=path.yaml,
    mode="r",
    encoding="utf-8",
  ) as file:
    content = file.read()
    content = os.path.expandvars(content)
    directory = os.path.join(
      os.path.dirname(path.yaml),
      'test_resources',
    )
    content = content.replace('$TEST_RESOURCES', directory)
    test_data = yaml.safe_load(content)

  return test_data


async def get_module_resources_and_tests(
  path: get_file_paths.FilePaths,) -> Module:
  module = Module()

  module.function_names = await get_function_definitions.main(
    module_path=str(path.python), output_attributes="name")

  module.functions = await get_test_data_from_yml(path=path)
  if not module.functions:
    module.functions = {}
  if "functions" in module.functions:
    module.functions = module.functions.get("functions")

  module.module = await get_module.main(location=path.python)
  module.module = await add_test_resources_to_module(
    module=module.module,
    path=path,
  )
  return module


# async def format_function_tests(module: Module) -> Module:
#   return module


# Fields that are set at the function and test levels
FORMAT_FIELDS = [
  "cast_arguments",
  "cast_result",
  "patch",
  "assertions",
]


async def format_function_and_test_data(module: Module) -> Module:
  functions = []
  for data in module.functions:
    function = await dacite_wrapper.main(
      object="from_dict",
      data={
        "data": data,
        "data_class": Function,
      },
    )

    function.module = module.module

    if not function.description:
      function.description = function.name

    if not function.assertions:
      module.assertions = [{"equals": False}]

    if function.tests is None:
      continue

    tests = []
    for test in function.tests:
      for field in FORMAT_FIELDS:
        if getattr(test, field):
          continue
        value = getattr(function, field)
        setattr(
          test,
          field,
          value,
        )

      if not test.description:
        count = len(tests)
        test.description = f"Test {count}"

      test.module = function.module
      test.function = function.name

      # Format as dict/kwargs for multi-threading
      test_formatted = {"test": test}
      tests.append(test_formatted)

    function.tests = tests
    functions.append(function)

  module.functions = functions
  return module


async def add_test_resources_to_module(
  module: ModuleType,
  path: get_file_paths.FilePaths,
) -> ModuleType:
  if not path.test_resources:
    return module

  for resource_path in path.test_resources:
    if resource_path.find('.py') == -1:
      continue

    directory = os.path.dirname(path.python)
    resource_tree = resource_path.replace(directory, "")
    resource_tree = resource_tree.split(os.sep)

    # Create the path to the resource in the module
    parent = module
    for root in resource_tree[1:-1]:
      if not hasattr(parent, root):
        setattr(parent, root, Store())
      parent = getattr(parent, root)

    # Add the resource to the path
    resource_module = await get_module.main(location=resource_path)
    resource_name = resource_tree[-1].replace(".py", "")
    setattr(parent, resource_name, resource_module)

  return module


async def execute_test(test: Test) -> Test:
  if test.patch:
    for patch_data in test.patch:
      patch_data.update({"module": test.module})
      test.module = await patch.main(**patch_data)

  if test.cast_arguments:
    for argument, caster in test.cast_arguments.items():
      value = test.arguments[argument]
      value = await cast.main(
        module=test.module,
        value=value,
        cast_as=caster,
      # TODO: Add switcher for unpacking based on value and caster
        unpack=True,
      )
      test.arguments[argument] = value

  function = getattr(test.module, test.function)
  try:
    test.result = function(**test.arguments)
  except (RuntimeError, Exception) as exception:
    test.exception = exception
    test.result = type(exception).__name__

  if type(test.result).__name__ == 'coroutine':
    test.result = await test.result


  if test.cast_result:
    test.result = await cast.main(
      module=test.module,
      value=test.result,
      cast_as=test.cast_result,
    )

  # test.passed = []
  results = []
  for assertion in test.assertions:
    result = await assertions.main(
      result=test.result,
      assertion=assertion,
    )
    # test.passed.append(result.passed)

    results.append(result.result)
  test.result = results

  test.module = test.module.__file__
  return test


async def setup_tests(data: Data) -> Data:
  modules = []
  for path in data.test_files:
    module = await get_module_resources_and_tests(path=path)
    module = await format_function_and_test_data(module=module)

    for function in module.functions:
      await multithread.main(
        target=execute_test,
        kwargs=function.tests,
      )

    modules.append(module)
  data.modules = modules
  return data


# ruff: noqa: ARG001
async def main(
  project_path: str | None = None,
  exclude_patterns: List[str] | None = None,
  text: str | None = None,
) -> Any:
  data = await format_main_arguments.main(
    _locals=locals(),
    data_classes={"body": Body},
    main_data_class=Data,
  )
  data.test_files = await get_file_paths.main(
    project_path=data.body.project_path,
    exclude_patterns=data.body.exclude_patterns + EXCLUDE_PATTERNS,
  )
  data = await setup_tests(data=data)
  return data


async def example() -> None:
  directory = os.path.dirname(MODULE_PATH)
  directory = os.path.join(directory, "example")

  text = f"""
    project_path: {directory}
    exclude_patterns:
    - ignore
    - test_resources
  """
  result = await main(text=text)
  print(result)


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
