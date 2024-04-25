#!/usr/bin/env python3
# encoding: utf-8

import asyncio
import os
from typing import List

import pytest
import yaml

import app.main as pytest_yaml

MODULE_PATH = __file__


def get_config(module_path: str) -> dict:
  yaml_path = module_path.replace('.py', '.yml')
  with open(
    file=yaml_path,
    mode='r',
    encoding='utf-8',
  ) as file:
    content = file.read()
    return yaml.safe_load(content)


CONFIG = get_config(module_path=MODULE_PATH)


def pytest_addoption(parser: pytest.Parser) -> None:
  for argument in CONFIG.get('cli_arguments'):
    parser.addoption(
      f"--{argument.get('args')}",
      **argument.get('options'),
    )

    ini_options = {'help': argument.get('options').get('help')}
    parser.addini(
      argument.get('args'),
      **ini_options,
    )


def get_project_path(config: pytest.Config) -> str:
  name = 'project-path'

  option = config.getoption(name.replace('-', '_'))
  ini = config.getini(name)
  directory = option if option else ini

  if directory in ['.', None]:
    return config.rootdir

  # Absolute directory path given relative directory path
  if directory.find('./') == 0:
    relative_path = directory.replace('./', '')
    return f'{config.rootdir}{os.sep}{relative_path}'

  return directory


def get_custom_assertions(config: pytest.Config) -> str:
  name = 'custom-assertions'

  directory = config.rootdir
  option = config.getoption(f'--{name}')
  ini = config.getini(name)

  directory = directory if not option else option
  directory = directory if not ini else ini
  return directory


def get_exclude_patterns(config: pytest.Config) -> List[str]:
  name = 'exclude-patterns'

  configs = [
    config.getoption(f'--{name}'),
    config.getini(name),
  ]

  exclusions = []
  for item in configs:
    if not item:
      continue
    if isinstance(item, list):
      exclusions.extend(item)
    if isinstance(item, str):
      exclusions.append(item)

  return exclusions


# ruff: noqa: ARG001
def get_yml_tests(
  project_path: str,
  exclude_patterns: List[str],
) -> List[pytest_yaml.Test]:
  test_results = asyncio.run(pytest_yaml.main(**locals()))
  tests = []

  for module in test_results.modules:
    for function in module.functions:
      for test in function.tests:
        tests.append(list(test.values())[0])

  # Handle no tests being collected
  if not tests:
    tests = [
      pytest_yaml.Test(
        module='',
        function='',
        description='',
        result='No tests collected',
        assertions=[{
          'equals': True,
        }],
      )
    ]

  return tests


def pytest_configure(config: pytest.Config) -> None:
  pytest.project_path = get_project_path(config=config)
  pytest.exclude_patterns = get_exclude_patterns(config=config)
  pytest.custom_assertions = get_custom_assertions(config=config)
  pytest.yml_tests = get_yml_tests(
    project_path=pytest.project_path,
    exclude_patterns=pytest.exclude_patterns,
  )


def pytest_itemcollected(item):
  params = item.callspec.params.get('test')

  module = params.module
  if not isinstance(module, str):
    module = module.__file__

  nodeid = [
    '\n',
    f'function: {params.function}\n',
    f'test: {params.description}\n',
    f'module: {module}\n',
    f"yml: {module.replace('.py', '_test.yml')}\n",
    'result:',
  ]
  nodeid = ''.join(nodeid)
  item._nodeid = nodeid
