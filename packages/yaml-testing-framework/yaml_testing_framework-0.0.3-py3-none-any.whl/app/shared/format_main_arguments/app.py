#!/usr/bin/env python3

import dataclasses as dc
import os
from typing import Dict

import yaml


@dc.dataclass
class DataClass:
  # General dataclass type hint
  ...


async def format_arguments(
  _locals: dict,
  data_classes: Dict[str, DataClass],
  main_data_class: DataClass,
) -> DataClass:
  store = {}
  for name, dataclass in data_classes.items():
    dataclass_instantiated = dataclass()
    for field in dc.fields(dataclass_instantiated):
      if field.name not in _locals:
        continue
      value = _locals[field.name]
      if value is None:
        continue
      setattr(
        dataclass_instantiated,
        field.name,
        value,
      )
    store[name] = dataclass_instantiated
  data = main_data_class(**store)
  return data


async def format_text_argument(data: DataClass) -> DataClass:
  if not hasattr(data.body, 'text'):
    return data

  if not data.body.text:
    return data

  text = os.path.expandvars(data.body.text)
  text = yaml.safe_load(text)

  for argument, value in text.items():
    if value is None:
      continue
    setattr(
      data.body,
      argument,
      value,
    )

  return data


async def main(
  _locals: dict,
  data_classes: Dict[str, DataClass] | None = None,
  main_data_class: DataClass | None = None,
) -> DataClass:
  data = await format_arguments(
    _locals=_locals,
    data_classes=data_classes,
    main_data_class=main_data_class,
  )
  data = await format_text_argument(data=data)
  return data
