# Dslog

> Dead-simple logging: just function composition

```python
from dslog import Logger

logger = Logger.of(print) \
  .limit('WARNING') \
  .format(lambda *objs, level, (f'[green][{level}][/]', *objs))

logger('My message', ..., level='INFO')
# doesn't print anything
logger('Oops!', { 'more': 'details' }, level='WARNING')
# [WARNING] Oops! { 'more', 'details' }     ([WARNING] in green)
```