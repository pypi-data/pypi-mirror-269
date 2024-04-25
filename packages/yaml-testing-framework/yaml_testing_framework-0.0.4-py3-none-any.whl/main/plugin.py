#!.venv/bin/python3
# -*- coding: utf-8 -*-

import os
from types import ModuleType
from types import SimpleNamespace as sns
from typing import Any, List

import pytest as py_test

from main.app import main as app
from main.utils import get_config, get_object


MODULE = __file__
CONFIG = get_config.main()
CONFIG.root_paths = [
  f'.{os.sep}',
  f'{os.sep}{os.sep}',
  f'.{os.sep}',
  *CONFIG.root_paths, ]
LOCALS = locals()


def get_options(
  options: dict,
  option_names: dict,
) -> dict:
  store = {}
  for name in option_names:
    option_name = name.replace('-', '_')
    store[option_name] = options.get(option_name)
  return store


def process_option_exclude_files(
  option: dict | None = None,
  config: py_test.Config | None = None,
) -> List[str]:
  _ = config

  option = option or []
  if not isinstance(option, list):
    option = [option]
  return option


def process_option_project_directory(
  option: str | None,
  config: py_test.Config,
) -> str:
  root = getattr(config, 'rootdir', '')
  root = str(root) or ''

  option = str(option)

  if option in CONFIG.root_paths:
    return root

  if option.find('.') == 0:
    option = os.path.join(root, option[1:])

  return os.path.normpath(option)


def get_pytest_parser(pytest_instance: ModuleType) -> py_test.Parser:
  pytest_instance = pytest_instance or get_pytest_instance()
  return pytest_instance.Parser


def get_pytest_instance(data: None = None) -> py_test:
  _ = data
  import pytest as instance
  return instance



def add_args_and_ini_options_to_parser(
  parser: py_test.Parser,
) -> py_test.Parser:
  for argument in CONFIG.options:
    parser.addoption(
      f"--{argument.get('args')}",
      **argument.get('options'),
    )
    ini_options = {'help': argument.get('options').get('help')}
    parser.addini(
      argument.get('args'),
      **ini_options,
    )
  return parser


def pytest_addoption(parser: py_test.Parser) -> None:
  add_args_and_ini_options_to_parser(parser=parser)


def pass_through(
  option: Any | None = None,
  config: py_test.Config | None = None,
) -> Any:
  _ = config
  return option


def pytest_configure(config: py_test.Config) -> None:
  data = {}

  names = [item['args'] for item in CONFIG.options]
  for name in names:
    option_name = f'--{name}'
    option = config.getoption(name=option_name)
    ini = config.getini(name)
    key = name.replace('-', '_')
    data[key] = option or ini

  py_test.yaml_tests = app(**data)
  py_test.yaml_tests = py_test.yaml_tests or []


def set_node_ids(item) -> str:
  if isinstance(item, dict):
    item = sns(**item)
  id_ = get_object.main(
    parent=item,
    route='callspec.params.test.id_short', )
  item._nodeid = str(id_).strip()
  return item


def pytest_itemcollected(item):
  item = set_node_ids(item=item)


def pytest_runtest_logreport(report):
  report.nodeid = format_report_nodeid(nodeid=report.nodeid)


def format_report_nodeid(nodeid: str) -> str:
  nodeid = str(nodeid)

  match = '<- test_entrypoint.py'
  index = nodeid.find(match)
  if index != -1:
    nodeid = nodeid[:index]

  match = 'test_['
  index = nodeid.find(match)
  if index != -1:
    nodeid = nodeid[index + len(match):]

  return nodeid.strip()


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
