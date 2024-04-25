#! /usr/bin/env python3

import dataclasses as dc
from typing import Any

import dacite

from app.shared.format_main_arguments import app as format_main_arguments


@dc.dataclass
class Body:
  object: str | None = None
  data: Any | None = None


@dc.dataclass
class Data:
  body: Body | None = None
  object: Any | None = None
  data: Any | None = None
  result: Any | None = None


def raise_exception(
  parent: object,
  child: str,
) -> None:
  message = f'Cannot get {child} from {type(parent).__name__}'
  raise RuntimeError(message)


GET_OBJECT = {
  'type': lambda parent, child: getattr(parent, child),
  'module': lambda parent, child: getattr(parent, child),
  'dict': lambda parent, child: parent[child],
  '*': raise_exception,
}


async def get_object(data: Data) -> Data:
  object_path = data.body.object.split('.')
  parent = dacite
  for path in object_path:
    parent_type = type(parent).__name__
    if parent_type not in GET_OBJECT:
      parent_type = '*'
    switcher = GET_OBJECT[parent_type]
    parent = switcher(parent=parent, child=path)
  data.object = parent
  return data


GET_RESULT = {'from_dict': lambda _object, data: _object(**data)}


async def get_result(data: Data) -> Data:
  name = data.body.object.split('.')[-1]
  switcher = GET_RESULT[name]
  data.result = switcher(
    _object=data.object,
    data=data.body.data,
  )
  return data


# ruff: noqa: ARG001
async def main(
  object: str | None = None,
  data: Any | None = None,
  text: str | None = None,
) -> Any:
  data = await format_main_arguments.main(
    _locals=locals(),
    data_classes={'body': Body},
    main_data_class=Data,
  )
  data = await get_object(data=data)
  data = await get_result(data=data)
  return data.result


async def example() -> None:

  @dc.dataclass
  class Example:
    one: int = 0
    two: int = 0

  data = {'data_class': Example, 'data': {'one': 1, 'two': 2}}
  result = await main(
    object='from_dict',
    data=data,
  )
  print(result)


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
