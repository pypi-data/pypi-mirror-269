#!/usr/bin/env python3

import dataclasses as dc
import time
from types import ModuleType
from typing import Any, Callable, Dict, List

# from app.shared.get_module import app as get_module_at_path
# import app.shared.format_main_arguments.app as format_main_arguments
import app.shared.get_module.app as get_module_at_path 
from app.shared.get_module import app as get_module_at_path

MODULE_PATH = __file__

SIDE_EFFECTS = {}


@dc.dataclass
class Object:
  parent: Any | None = None
  name: str | None = None


@dc.dataclass
class Data_2:
  module: str | None = None
  object_parent: Any | None = None
  object_name: str | None = None
  method: str | None = None
  patch: Any | None = None
  value: Any | None = None


async def setup_2(_locals: dict) -> Data_2:
  data = Data_2()
  for key, value in _locals.items():
    if not hasattr(data, key) or value is None:
      continue
    setattr(data, key, value)
  return data


async def get_module_2(module: ModuleType | str) -> Data_2:
  if isinstance(module, str):
    module = await get_module_at_path.main(location=module)
  return module


async def get_value_patch(value: Any) -> Any:
  def patch(value: Any) -> Any:
    return value
  return patch(value=value)


async def get_return_patch(value: Any) -> Callable:
  # ruff: noqa: ARG001
  def return_patch(*args, **kwargs) -> Any:
    return value
  return return_patch


async def get_side_effect_list_patch(value: List) -> Callable:
  timestamp = int(time.time())

  global SIDE_EFFECTS
  SIDE_EFFECTS[timestamp] = List_Side_Effect(
    values=value, count=0)

  # ruff: noqa: ARG001
  def side_effect_list_patch(*args, **kwargs) -> Any:
    n = len(SIDE_EFFECTS[timestamp].values)
    if SIDE_EFFECTS[timestamp].count == n:
      SIDE_EFFECTS[timestamp].count = 0
    SIDE_EFFECTS[timestamp].count += 1
    return SIDE_EFFECTS[timestamp].values[SIDE_EFFECTS[timestamp].count - 1]

  return side_effect_list_patch


async def get_side_effect_dict_patch(value: dict) -> Callable:
  def side_effect_dict_patch(key) -> Any:
    return value[key]
  return side_effect_dict_patch


async def get_patch_2(
  method: str,
  value: Any,
  _locals: dict = locals(),
) -> Any:
  function = f'get_{method}_patch'
  function = _locals[function]
  patch = await function(value=value)
  return patch


async def get_object_from_dict_2(
  object_parent: dict,
  object_name: str,
) -> Any:
  if object_name in object_parent:
    return object_parent[object_name]

  if object_name not in object_parent:
    object_parent[object_name] = Store()
    return object_parent[object_name]


async def get_object_from_module_2(
  object_parent: object,
  object_name: str,
) -> Any:
  if hasattr(object_parent, object_name):
    return getattr(object_parent, object_name)

  if hasattr(object_parent, '__builtins__'):
    if hasattr(object_parent.__builtins__, object_name):
      return getattr(object_parent.__builtins__, object_name)

  setattr(object_parent, object_name, Store())
  return getattr(object_parent, object_name)


async def get_object_from_other_2(
  object_parent: object,
  object_name: str,
) -> None:
  # message = f'{type(object_parent).__name__} has no object {object_name}'
  # raise RuntimeError(message)
  return


GET_OBJECT = {
  'module': get_object_from_module_2,
  'Store': get_object_from_module_2,
  'dict': get_object_from_dict_2,
  '*': get_object_from_other_2,
}


async def get_object_2(
  data: Data_2,
  _locals: dict = locals(),
) -> Data_2:
  paths = object.split('.')
  n = len(paths)

  if n == 1:
    data.object_name = paths[0]
    return data

  for object_name in paths[:-1]:
    kind = type(data.object_parent).__name__.lower()
    if kind not in ['module', 'store', 'dict', 'moduletype']:
      kind = '*'

    function = f'get_object_from_{kind}_2'
    function = _locals[function]
    data = await function(data=data)

  return data


async def patch_dict_object(data: Data_2) -> Data_2:
  data.object_parent[data.object_name] = data.patch
  return data


async def patch_object_object(data: Data_2) -> Data_2:
  setattr(data.object_parent, data.object_name, data.patch, )
  return data


async def patch_object_2(
  data: Data_2,
  _locals: dict = locals(),
) -> Data_2:
  kind = type(data.object_parent).__name__
  kind = 'object' if kind != 'dict' else kind

  function = f'path_{kind}_object'
  function = _locals[function]
  data.object_parent = await function(data=data)
  return data


async def main_2(
  module: str | None = None,
  object_parent: Any | None = None,
  object_name: str | None = None,
  method: str | None = None,
  patch: Any | None = None,
  value: Any | None = None,
) -> Any:
  data = await setup_2(_locals=locals())
  data = await get_module_2(data=data)
  data = await get_patch_2(data=data)
  data = await get_object_2(data=data)
  data = await patch_object_2(data=data)
  return data.module


async def example() -> None:
  result = main(
    module=MODULE_PATH,
    object='int',
    method='value',
    value='value',
  )
  print(result)


if __name__ == '__main__':
  import asyncio


  asyncio.run(example())



####################################


# @dc.dataclass
# class Body:
#   module: str | None = None
#   object: str | List[str] | None = None
#   return_value: Any | None = None
#   value: Any | None = None
#   side_effect_list: List | None = None
#   side_effect_dict: Dict | None = None
#   text: str | None = None


# @dc.dataclass
# class Object:
#   parent: Any | None = None
#   name: str | None = None


# @dc.dataclass
# class Data:
#   body: Body | None = None
#   patch: Any | None = None
#   object: Object | object | None = None
#   module: str | ModuleType | None = None
#   call_method: str = 'module'


# @dc.dataclass
# class List_Side_Effect:
#   values: List[Any] | None = None
#   count: int | None = None


# class Store:
#   pass


# async def get_module(data: Data) -> Data:
#   # data.module = runpy.run_path(path_name=data.body.module)
#   module_type = type(data.body.module).__name__
#   if module_type in ['module', 'ModuleType']:
#     data.module = data.body.module
#     return data

#   if module_type == 'str':
#     data.module = await get_module_at_path.main(location=data.body.module)
#     return data


# async def get_patch_for_value(data: Data) -> Any:
#   def patch(value: Any) -> Any:
#     return value
#   return patch(value=data.body.value)


# async def get_patch_for_return_value(data: Data) -> Callable:
#   # ruff: noqa: ARG001
#   def patch(*args, **kwargs) -> Any:
#     return data.body.return_value

#   return patch


# async def get_patch_for_side_effect_list(data: Data) -> Callable:
#   timestamp = int(time.time())

#   global SIDE_EFFECTS
#   SIDE_EFFECTS[timestamp] = List_Side_Effect(
#     values=data.body.side_effect_list, count=0)

#   # ruff: noqa: ARG001
#   def patch(*args, **kwargs) -> Any:
#     n = len(SIDE_EFFECTS[timestamp].values)
#     if SIDE_EFFECTS[timestamp].count == n:
#       SIDE_EFFECTS[timestamp].count = 0
#     SIDE_EFFECTS[timestamp].count += 1
#     return SIDE_EFFECTS[timestamp].values[SIDE_EFFECTS[timestamp].count - 1]

#   return patch


# async def get_patch_for_side_effect_dict(data: Data) -> Callable:

#   def patch(key) -> Any:
#     return data.body.side_effect_dict[key]

#   return patch


# CREATE_PATCH = {
#   'value': get_patch_for_value,
#   'return_value': get_patch_for_return_value,
#   'side_effect_list': get_patch_for_side_effect_list,
#   'side_effect_dict': get_patch_for_side_effect_dict,
# }


# async def create_patch(data: Data) -> Data:
#   cases = [
#     'value' if data.body.value is not None else '',
#     'return_value' if data.body.return_value is not None else '',
#     'side_effect_list' if data.body.side_effect_list is not None else '',
#     'side_effect_dict' if data.body.side_effect_dict is not None else '',
#   ]
#   cases = ''.join(cases)
#   switcher = CREATE_PATCH[cases]
#   data.patch = await switcher(data=data)
#   return data


# async def get_object_from_module(parent, child) -> Any:
#   cases = [
#     'module' if hasattr(parent, child) else '',
#     'builtins' if hasattr(parent.__builtins__, child) else '',
#   ]
#   cases = ''.join(cases)

#   if hasattr(parent, child):
#     child = getattr(parent, child)
#     return child

#   if hasattr(parent.__builtins__, child):
#     child = getattr(parent.__builtins__, child)
#     return child

#   if not hasattr(parent, child):
#     setattr(parent, child, Store())
#     child = getattr(parent, child)
#     return child


# async def get_object_from_dictionary(parent, child) -> Any:
#   if child in parent:
#     return parent[child]
#   if child not in parent:
#     parent[child] = Store()
#     return parent[child]


# async def get_object_from_other(parent, child) -> Any:
#   message = f'{type(parent).__name__} has no object {child}'
#   raise RuntimeError(message)


# GET_OBJECT = {
#   'module': get_object_from_module,
#   'Store': get_object_from_module,
#   'dict': get_object_from_dictionary,
#   '*': get_object_from_other,
# }


# async def get_object(data: Data) -> Data:
#   paths = data.body.object.split('.')
#   n = len(paths)

#   parent = data.module

#   if n == 1:
#     data.object = Object(parent=parent, name=paths[0])
#     return data

#   for path in paths[:-1]:
#     parent_type = type(parent).__name__
#     if parent_type not in GET_OBJECT:
#       parent_type = '*'

#     switcher = GET_OBJECT[parent_type]
#     parent = await switcher(
#       parent=parent,
#       child=path,
#     )

#   data.object = Object(parent=parent, name=paths[-1])
#   return data


# async def patch_object(data: Data) -> Data:
#   parent_type = type(data.object.parent).__name__

#   if parent_type == 'dict':
#     data.object.parent[data.object.name] = data.patch
#     return data

#   if parent_type in ['module', 'Store']:
#     setattr(
#       data.object.parent,
#       data.object.name,
#       data.patch,
#     )
#     return data


# # ruff: noqa: ARG001
# async def main(
#   module: str | ModuleType | None = None,
#   object: str | object | None = None,
#   return_value: Any | None = None,
#   value: Any | None = None,
#   side_effect: List | Dict | None = None,
#   text: str | None = None,
# ) -> dict:
#   data = await format_main_arguments.main(
#     _locals=locals(),
#     data_classes={'body': Body},
#     main_data_class=Data,
#   )
#   data = await get_module(data=data)
#   data = await create_patch(data=data)
#   data = await get_object(data=data)
#   data = await patch_object(data=data)
#   return data.module


async def example() -> None:
  import os

  text = f'''
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: add
    return_value: add_patched
    value:
    side_effect:
  '''
  module = await main_2(text=text)
  print(module.add(1, 2))
  print(module.use_add())

  text = f'''
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: patch_os
    value: patch_os_patched
  '''
  module = await main(text=text)
  print(module.patch_os)

  text = f'''
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: os.patch_os
    value: os.patch_os_patched
  '''
  module = await main(text=text)
  print(module.os.patch_os)

  text = f'''
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: dictionary_module.add
    value: dictionary_module.add_patched
  '''
  module = await main(text=text)
  print(module.dictionary_module['add'])

  text = f'''
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: test2.test1
    value: test2.test1_patched
  '''
  module = await main(text=text)
  print(module.dictionary_module['test2']['test1'])

  text = f'''
    module: {os.path.dirname(MODULE_PATH)}/test_resources/app.py
    object: side_effect_list
    side_effect_list: [side_effect_1, side_effect_2]
  '''
  module = await main(text=text)
  print(
    module.side_effect_list(),
    module.side_effect_list(),
    module.side_effect_list(),
  )


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
