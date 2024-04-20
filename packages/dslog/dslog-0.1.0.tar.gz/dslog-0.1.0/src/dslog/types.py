from typing import Protocol, Literal, Iterable

Level = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
LEVELS: dict[Level, int] = {
    'DEBUG': 10,
    'INFO': 20,
    'WARNING': 30,
    'ERROR': 40,
    'CRITICAL': 50,
}

def value(level: Level | int) -> int:
  return level if isinstance(level, int) else LEVELS[level]

class Handler(Protocol):
  """Just prints out shit"""
  def __call__(self, *objs):
    ...

class Formatter(Protocol):
  """Formats log inputs"""
  def __call__(self, *objs, level: Level) -> Iterable:
    ...

