#!.venv/bin/python3
# -*- coding: utf-8 -*-

import os
import sys

import nest_asyncio


MODULE = __file__
MAIN_DIR = os.path.dirname(__file__)
DIRECTORIES = dict(main=MAIN_DIR)
EXCLUDE_DIRECTORIES = ['.ignore', '__pycache__', ]


def allow_nested_event_loops() -> int:
  nest_asyncio.apply()
  return 1


def add_directories_to_pythonpath(directories: None = None) -> int:
  directories = directories or DIRECTORIES
  root = os.path.dirname(__file__)

  for key, value in directories.items():
    path = os.path.join(root, value)
    if path not in sys.path:
      sys.path.append(path)

  return 1


allow_nested_event_loops()
add_directories_to_pythonpath()


def examples() -> None:
  from main.utils import invoke_testing_method

  invoke_testing_method.main()


if __name__ == '__main__':
  examples()
