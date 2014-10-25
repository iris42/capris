capris
======

Capris is an extremely simple and friendly wrapper
around the ``subprocess.Popen`` interface. It is
heavily inspired by ``envoy``. The API is extremely
simple:

```python
from capris import run
response = run([['echo', 'hello'], ['cat']])
```
