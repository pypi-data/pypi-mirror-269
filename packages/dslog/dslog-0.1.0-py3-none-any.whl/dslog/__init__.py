"""
### Dslog
> Dead-simple logging: just function composition

```
from dslog import Logger

logger = Logger.of(rich.print) \\
  .limit('WARNING') \\
  .format(lambda level, *objs, (f'[green][{level}][/]', *objs))

logger('My message', ..., level='INFO')
# doesn't print anything
logger('Oops!', { 'more': 'details' }, level='WARNING')
# [WARNING] Oops! { 'more', 'details' }     ([WARNING] in green)
```
"""
from .types import Level
from .logger import Logger, LogFn