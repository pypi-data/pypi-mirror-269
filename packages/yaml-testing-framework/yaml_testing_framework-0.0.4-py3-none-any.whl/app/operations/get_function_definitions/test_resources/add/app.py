#! /usr/bin/env python3

import dataclasses as dc


@dc.dataclass
class Data:
  a: int = 0
  b: int = 0


def add_numbers(_locals: dict) -> int:
  return _locals["a"] + _locals["b"]


def add_dataclass(_locals: dict) -> int:
  data = _locals["data"]
  return data.a + data.b


MAIN = {
  "dataclass": add_dataclass,
  "int": add_numbers,
}


def main(
  data: Data | dict | None = None,
  a: int | float | None = None,
  b: int | float | None = None,
) -> int:
  cases = "dataclass" if data else "numbers"
  switcher = MAIN[cases]
  data = switcher(data=data)
  return data


if __name__ == '__main__':
  data = Data(1, 2)
  result = main(data)
  print(result)
