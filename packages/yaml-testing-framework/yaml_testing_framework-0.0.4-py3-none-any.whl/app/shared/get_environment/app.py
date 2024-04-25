#!/usr/bin/env python3

import dataclasses as dc
import os
from typing import Dict

import yaml


@dc.dataclass
class Env:
  ...


@dc.dataclass
class Data:
  config: dict | None = None
  module_path: str | None = None
  yml_path: str | None = None
  environment_key: str = 'environment'
  env: Env | dict | None = None


def format_arguments(_locals: dict) -> Data:
  data = Data()
  for field in dc.fields(data):
    value = _locals.get(field.name)
    if not value:
      continue
    setattr(data, field.name, value)
  return data


def get_yml_path(data: Data) -> Data | None:
  if data.config or data.yml_path:
    return data

  if not data.yml_path:
    data.yml_path = data.module_path.replace('.py', '.yml')
    return data


def get_environment_data(data: Data) -> Data:
  if data.config:
    data.config = data.config.get(data.environment_key)
    return data

  data.config = {}

  with open(
    file=data.yml_path,
    mode='r',
    encoding='utf-8',
  ) as file:
    content = file.read()
    data.config = yaml.safe_load(content)

  data.config = data.config.get(data.environment_key)
  return data


def convert_dict_to_dataclass(data: Data) -> Env:
  fields = []
  for key, value in data.config.items():
    field = (
      key,
      str,
      dc.field(default=value),
    )
    fields.append(field)
  data.env = dc.make_dataclass('Env', fields)()
  return data


def get_variables_from_venv(data: Data) -> Data:
  for key in data.config:
    venv_value = os.getenv(key)
    if venv_value is None:
      continue
    data.config[key] = venv_value
  return data


# ruff: noqa: ARG001
def main(
  module_path: str | None = None,
  config: dict | None = None,
  yml_path: str | None = None,
  environment_key: str = 'environment',
) -> Env:
  data = format_arguments(_locals=locals())
  data = get_yml_path(data=data)
  data = get_environment_data(data=data)
  data = get_variables_from_venv(data=data)
  data = convert_dict_to_dataclass(data=data)
  return data.env


def example() -> None:
  yml_path = '${WORKDIR}/utils/get_environment/test_resources/app.yml'
  result = main(yml_path=yml_path)
  print(result)


if __name__ == '__main__':
  example()
