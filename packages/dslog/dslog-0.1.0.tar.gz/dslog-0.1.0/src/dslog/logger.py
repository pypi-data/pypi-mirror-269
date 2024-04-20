from typing import Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
from .types import Level, Handler, Formatter, value

class LogFn(Protocol):
  def __call__(self, *objs, level: Level = 'INFO'):
    ...

class Logger(ABC, LogFn):
  @abstractmethod
  def __call__(self, *objs, level: Level = 'INFO'):
    ...

  @classmethod
  def of(cls, handler: Handler) -> 'Logger':
    return LoggerOf(handler)
  
  @classmethod
  def empty(cls) -> 'Logger':
    """A logger that doesn't do anything"""
    return LoggerOf(lambda *_, **_kw: None)

  def limit(self, min_level: Level) -> 'Logger':
    return Limited(min_level, self)
  
  def format(self, format: Formatter) -> 'Logger':
    return Formatted(format, self)
  
  def prefix(self, prefix: str) -> 'Logger':
    return self.format(lambda *objs, **_: (prefix, *objs))
  
  def postfix(self, postfix: str) -> 'Logger':
    return self.format(lambda *objs, **_: (*objs, postfix))
  
@dataclass
class LoggerOf(Logger):
  handler: Handler
  def __call__(self, *objs, **_):
    self.handler(*objs)

@dataclass
class Limited(Logger):
  min_level: Level | int
  logger: Logger

  def __call__(self, *objs, level: Level = 'INFO'):
    if value(level) >= value(self.min_level):
      self.logger(level, *objs)

@dataclass
class Formatted(Logger):
  formatter: Formatter
  logger: Logger

  def __call__(self, *objs, level: Level = 'INFO'):
    formatted_objs = self.formatter(*objs, level=level)
    self.logger(*formatted_objs, level=level)