#!/usr/bin/env python3

import copy
import dataclasses as dc
from typing import Any


@dc.dataclass
class Data:
  assertion: dict | None = None
  result: Any | None = None


async def assert_equals(data: Data) -> Data:
  data.result = {'equals': data.result}
  return data


async def assert_type(data: Data) -> Data:
  result_type = type(data.result).__name__
  assertion_type = data.assertion.get('type')

  types = copy.deepcopy(assertion_type)
  if not isinstance(types, list):
    types = [types]

  if result_type in types:
    data.result = {'type': assertion_type}
  if result_type not in types:
    data.result = {'type': result_type}

  return data


async def assert_has_attributes(data: Data) -> Data:
  has_attributes = data.assertion.get('has_attributes')
  result = {}

  for key, value in has_attributes.items():
    assert_value = None
    if hasattr(data.result, key):
      assert_value = getattr(data.result, key)
    result[key] = assert_value

  data.result = {'has_attributes': result}
  return data


async def assert_has_keys(data: Data) -> Data:
  has_keys = data.assertion.get('has_keys')
  result = {}

  for key, value in has_keys.items():
    assert_value = None
    if key in data.result:
      assert_value = data.result.get(key)
    result[key] = assert_value

  data.result = {'has_keys': result}
  return data


async def assert_length(data: Data) -> Data:
  data.result = {'length': len(data.result)}
  return data


ASSERTIONS = {
  'equals': assert_equals,
  'type': assert_type,
  'has_attributes': assert_has_attributes,
  'has_keys': assert_has_keys,
  'length': assert_length,
}


# ruff: noqa: ARG001
async def main(
  assertion: dict | None = None,
  result: Any | None = None,
  text: str | None = None,
) -> Any:
  data = Data(assertion=assertion, result=result)
  cases = list(data.assertion.keys())[0]
  switcher = ASSERTIONS[cases]
  data = await switcher(data=data)
  return data


async def example() -> None:
  import yaml


  tests = [
    '''
    assertion:
      equals: test
    result: test
    ''',
    '''
    assertion:
      type: str
    result: test
    ''',
    '''
    assertion:
      has_keys:
        test: test
    result:
      test: test
    ''',
  ]
  for text in tests:
    text = yaml.safe_load(text)
    result = await main(**text)
    print(result)


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
