#!/usr/bin/env python3

import dataclasses as dc
import glob
import os
from typing import List

from app.shared.get_environment import app as get_environment

PROJECT_PATH = os.path.abspath(os.curdir)
MODULE_PATH = __file__
ENV = get_environment.main(module_path=MODULE_PATH)

YAML_EXTENSIONS = ['_test.yaml', '_test.yml']
EXCLUDE_PATTERNS = [
  '.venv',
  '.eggs',
  'build',
  '_ignore',
  'ignore',
  'test_entrypoint.py',
  'plugin.py',
  'test_resources',
  '__pycache__',
  # '.pyc',
]


@dc.dataclass
class FilePaths:
  python: str | None = None
  yaml: str | None = None
  test_resources: List[str] | None = None


@dc.dataclass
class Data:
  project_path: str | None = None
  exclude_patterns: List[str] | None = None
  file_paths: List[FilePaths] | List[str] | None = None


async def set_project_path(project_path: str | None) -> str:
  if not project_path:
    project_path = PROJECT_PATH
  return project_path


SET_EXCLUDE_PATTERNS = {
  'str': lambda exclude_patterns: [exclude_patterns, *EXCLUDE_PATTERNS],
  'list': lambda exclude_patterns: exclude_patterns + EXCLUDE_PATTERNS,
  'NoneType': lambda exclude_patterns: EXCLUDE_PATTERNS,
}


async def set_exclude_patterns(
  exclude_patterns: str | List[str] | None = None,
) -> List[str]:
  patterns_type = type(exclude_patterns).__name__
  switcher = SET_EXCLUDE_PATTERNS[patterns_type]
  exclude_patterns = switcher(exclude_patterns=exclude_patterns)
  return exclude_patterns


async def get_python_file_paths(
  project_path: str,
  exclude_patterns: List[str] | None = None,
) -> List[str]:
  if os.path.isfile(project_path):
    return [project_path]

  file_paths = []
  for walks in os.walk(project_path):
    match = os.path.join(walks[0], '*.py')
    paths = glob.glob(match)

    for path in paths:
      exclude = False
      for pattern in exclude_patterns:
        if path.find(pattern) != -1:
          exclude = True
          break

      if exclude is True:
        continue
      file_paths.append(path)
  return file_paths


async def get_yaml_path(python_path: str) -> str:
  for extension in YAML_EXTENSIONS:
    yaml_path = python_path.replace('.py', extension)
    if not os.path.exists(yaml_path):
      continue
    return yaml_path


async def get_test_resource_paths(python_path: str) -> List[str]:
  directory = os.path.dirname(python_path)
  directory = os.path.join(directory, 'test_resources')
  match = os.path.join(directory, '*')
  paths = glob.glob(match)
  return paths


# ruff: noqa: ARG001
async def main(
  project_path: str | None = None,
  exclude_patterns: str | List[str] | None = None,
) -> Data:
  data = Data()
  data.project_path = await set_project_path(project_path=project_path)
  data.exclude_patterns = await set_exclude_patterns(
    exclude_patterns=exclude_patterns,)

  data.file_paths = await get_python_file_paths(
    project_path=data.project_path,
    exclude_patterns=data.exclude_patterns,
  )

  file_paths = []
  for i in range(len(data.file_paths)):
    python_path = data.file_paths[i]
    paths = FilePaths(
      python=python_path,
      yaml=await get_yaml_path(python_path=python_path),
      test_resources=await get_test_resource_paths(python_path=python_path),
    )
    file_paths.append(paths)

  return file_paths


async def example() -> None:
  result = await main()
  print(result)


if __name__ == '__main__':
  import asyncio

  asyncio.run(example())
