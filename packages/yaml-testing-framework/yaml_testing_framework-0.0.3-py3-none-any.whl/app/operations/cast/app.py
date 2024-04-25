#! /usr/bin/env python3

import dataclasses as dc
import json
from types import ModuleType
from typing import Any

# import app.shared.error_handler.app as error_handler


@dc.dataclass
class Data:
  value: Any | None = None
  value_type: str | None = None
  cast_as: str | None = None
  unpack: bool = False
  module: ModuleType | None = None
  caster: Any | None = None
  result: Any | None = None


async def setup(_locals: dict) -> Data:
  data = Data()
  for key, value in _locals.items():
    if not hasattr(data, key) or value is None:
      continue
    setattr(data, key, value)
  return data


async def get_caster_from_module(data: Data) -> object:
  paths = data.cast_as.split('.')

  caster = None

  if hasattr(data.module, paths[0]):
    caster = getattr(data.module, paths[0])

  if paths[0] in data.module.__builtins__:
    caster = data.module.__builtins__[paths[0]]

  if caster is None:
    return caster

  for path in paths[1:]:
    caster = getattr(caster, path)
  # print('CASTER', str(caster), type(caster).__name__)
  return caster


# async def cast_wildcard_to_wildcard(data: Data) -> Data:
#   return data


# async def cast_dict_to_dataclass(data: Data) -> Data:
#   data.result = data.caster(**data.value)
#   return data


# async def cast_list_to_dataclass(data: Data) -> Data:
#   data.result = data.caster(*data.value)
#   return data


# async def cast_str_to_dict(data: Data) -> Data:
#   data.result = json.loads(data.value)
#   return data


# async def cast_dict_to_str(data: Data) -> Data:
#   data.result = json.dumps(data)
#   return data


# async def cast_list_to_dict(data: Data) -> Data:
#   data.result = []
#   for value in data.value:
#     if dc.is_dataclass(value):
#       value = dc.asdict(value)
#       data.result.append(value)
#       continue

#     value = value.__dict__
#     data.result.append(value)
#   return data


# async def cast_object_as_str(data: Data) -> Data:
#   data.result = str(data.value)
#   return data


# CAST_VALUE = {
#   '*.*': cast_wildcard_to_wildcard,
#   'dict.dataclass': cast_dict_to_dataclass,
#   'list.dataclass': cast_list_to_dataclass,
#   'tuple.dataclass': cast_list_to_dataclass,
#   'str.dict': cast_str_to_dict,
#   'dict.str': cast_dict_to_str,
#   'list.dict': cast_list_to_dict,
#   'tuple.dict': cast_list_to_dict,
#   '*.str': cast_object_as_str,
# }


async def get_value_type(value: Any) -> str:
  _type = type(value).__name__.lower()
  _type = 'dataclass' if dc.is_dataclass(value) else _type
  _type = _type.lower()
  if _type not in [
    'list',
    'tuple',
    'dict',
    'dataclass',
    'nonetype',
  ]:
    _type = '*'
  return _type


SWITCHER = '''
- dataclass.dict.*
- dict.*.false
- dict.*.true
- str.dict*
- str.*
- list.str.*
- tuple.str.*
- list.*.*
- tuple.*.*
'''


async def cast_value(data: Data) -> Data:
  data.caster = await get_caster_from_module(data=data)

  # value_type.cast_as.unpack
  cases = [
    data.value_type,
    # data.cast_as,
    str(data.unpack),
  ]
  cases = '.'.join(cases).lower()
  # print(cases)


  if data.value_type == 'nonetype':
    data.result = data.value
    return data

  # dataclass.dict
  if data.value_type == 'dataclass' and data.cast_as == 'dict':
    # print(cases)
    data.result = dc.asdict(data.value)
    return data

  # *.false
  if data.value_type not in ['list', 'tuple', 'dict']:
    data.result = data.caster(data.value)
    return data

  if data.unpack and data.value_type == 'dict':
    data.result = data.caster(**data.value)
    return data

  if not data.unpack and data.value_type == 'dict':
    data.result = data.caster(data.value)
    return data

  if data.unpack and data.value_type in ['list', 'tuple']:
    data.result = data.caster(*data.value)
    return data

  if not data.unpack and data.value_type in ['list', 'tuple']:
    data.result = data.caster(data.value)
    return data

  message = f'Cannot cast {data.value_type} as {data.cast_as}'
  raise RuntimeError(message)


# ruff: noqa: ARG001
async def main(
  value: Any | None = None,
  cast_as: str | None = None,
  unpack: bool | None = None,
  module: ModuleType | None = None,
) -> Any:
  data = await setup(_locals=locals())
  data.caster = await get_caster_from_module(data=data)
  data.value_type = await get_value_type(value=data.value)
  data = await cast_value(data=data)
  return data.result


async def example() -> None:
  text = '''
    value: 1
    cast_as: Data
    source_code: |
      import dataclasses as dc
      from typing import Any


      @dc.dataclass
      class Data:
        value: Any | None = None

      def to_str(value):
        return str(value)
  '''
  result = await main(text=text)
  print(result)

  text = '''
    value: [1, 2, 3]
    unpack: true
    cast_as: to_str
    source_code: |
      import dataclasses as dc
      from typing import Any

      def to_str(x1, x2, x3):
        return f'{x1} {x2} {x3}'
  '''
  result = await main(text=text)
  print(result, type(result).__name__)

  text = '''
    value: 1
    cast_as: str
    source_code: |
      # no code
  '''
  result = await main(text=text)
  print(result, type(result).__name__)


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
