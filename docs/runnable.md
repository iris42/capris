# Runnables

Runnables are basically objects in the `capris` API
which have a `run` method. The base class `Runnable`
doesn't implement the method by raising a `NotImplementedError`
but all subclasses are expected to implement the
`run` method, as well as the `iter` and `str` magic
methods. For example:

```python
class SimpleCommand(Runnable):
    def __init__(self, command):
        self.command = command

    def __iter__(self):
        yield self.command

    def __str__(self):
        return str(self.command)

    def run(self):
        return os.system(self.command)
```

Runnables come in three flavours in the `capris`
API- commands, pipes, and iostreams. There are
some operator overloaded properties for them:

 - `|` operator
 - `iostream` property
    - `>` operator
    - `<` operator
    - `&` operator

Basically, to pipe the output of a runnable to
another using the `capris` DSL, you can use the
`|` operator, provided that the runnable's `run`
method returns a `capris.core.Response` object.
For example, the following do the same things:

```python
echo('pattern') | grep('pattern')
Pipe(echo('pattern'), grep('pattern'))
```

But the `|` operator will mutate the previous
`Pipe` object if you pipe a `Pipe` object and
a runnable, so it's recommended that you only
use the `|` operator when you do not need fine
grained control as the `|` operator is designed
to reduce the number of objects created.

The `iostream` property returns an `IOStream`
object for the runnable that you can hook callbacks
or redirect files to, for example to do the
following in `capris`:

```bash
$ cat file.txt > echo
```

We can do either of the following, which are both
equivalent but the `iostream` variant reduces
the overhead because one less process needs to
be spawned.

```python
cat('file.txt') | echo
open('file.txt') > echo.iostream
```

To redirect the output to another file-like object
we need to use the `>` operator, for example:

```python
echo('something').iostream > open('res.txt', 'w')
```

To assign callbacks that could be ran after the
command has completed execution succesfully (without
raising any exceptions), we can use the `&` operator,
for example for testing purposes:

```python
def callback(response):
    assert response.ok()
    assert response.std_out == 'pattern\n'

echo('something').iostream & callback
```
