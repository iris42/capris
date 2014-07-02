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
