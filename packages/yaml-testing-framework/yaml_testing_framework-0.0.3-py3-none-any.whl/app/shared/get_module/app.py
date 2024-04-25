#!/usr/bin/env python3

import dataclasses as dc
import importlib
import os
from types import ModuleType

MODULE_PATH = __file__


@dc.dataclass
class Module:
  location: str | None = None
  name: str | None = None
  object: ModuleType | None = None


async def set_module_name(module: Module) -> Module:
  if module.name:
    return module

  if not module.name:
    module.name = os.path.splitext(module.location)[0]
    module.name = os.path.basename(module.name)
    return module


async def load_module_from_location(module: Module) -> Module:
  spec = importlib.util.spec_from_file_location(
    name=module.name,
    location=module.location,
  )
  module.object = importlib.util.module_from_spec(spec)
  spec.loader.exec_module(module.object)
  return module


# ruff: noqa: ARG001
async def main(
  location: str,
  name: str | None = None,
) -> ModuleType:
  module = Module(location=location, name=name)
  module = await set_module_name(module=module)
  module = await load_module_from_location(module=module)
  return module.object


async def example() -> None:
  directory = os.path.dirname(MODULE_PATH)
  location = os.path.join(directory, "test_resources", "app.py")
  module = await main(location=location)
  print(module)


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
