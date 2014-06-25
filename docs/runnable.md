## `commandeer.Runnable`

The `Runnable` class represents a `run`-able object, or
an object that supports the `run` API. All `Pipe`s, `Command`s,
and `IOContext`s are subclasses of the `Runnable` class,
and have a `run` method.

 - `Runnable.run`
 - `Runnable.iostream`
 - `Runnable.__or__`

### `Runnable.run(*args, **kwargs)`

Exceutes the runnable object regardless if it's a `Pipe`
or `Command` or `IOContext` and returns a response depending
on whether it is a transaction-based command. For example:

```python
>>> git.log(graph=None).run()
<Response [git]>
```

Any keyword or positional arguments passed will be passed to
the `envoy.run` function.

### `Runnable.iostream`

A property that returns a `IOContext` instance that can
redirect output/input to the given runnable. For example:

```python
>>> iostream = git.log(n=20).iostream > open('file.txt', 'w')
>>> iostream.run()
```

### `Runnable.__or__(other)`

You can pipe `Runnable` objects by using the `|` operator,
instead of building up the pipe object manually. For
example:

```python
>>> git.log(graph=None) | grep('pattern') | wc
<Pipe [git log --graph | grep 'pattern' | wc]>
```

The `__or__` magic method is smart and will not build up more
than one `Pipe` object if it is used properly, by type checking.
