# Capris

`capris` is a DSL for creating beautiful apps that leverage
the command line in Python. `capris` purely generates commands
and runs them. A simple example of `capris` at work:

```python
from capris import *
git = Command('git')
grep = Command('grep')

pipe = git.log(graph=None) | grep('commit: [a-f0-9]\{40\}')
response = pipe.run()
```

There are three base classes in `capris`- `Command`, `Pipe`,
and `IOContext`. If you are not piping commands or doing
redirection you are most likely to just use the `Command`
class.

## `capris.command.Command`

A `Command` object represents a single command which can be
chained to create readable subcommands. It only has a few
methods and inherits from the base `Runnable` class:

 - `Command.copy`
 - `Command.subcommand`

### `Command.copy()`

This function is called whenever the command object itself
is called (via the `__call__` magic method), in order to
create a copy of the command and then apply changes to
the returned copy. For example:

```python
>>> copy = command.copy()
>>> str(copy) == str(command)
True
>>> copy is command
False
```

### `Command.subcommand(command)`

This method is invoked whenever you perform a `getattr` on
the command object and request for an attribute that is not
present. For example, the following are equivalent:

```python
>>> git.log
<Command [git log]>
>>> git.subcommand('log')
<Command [git log]>
```

Note that if you do a `getattr`-style command, the function
will automatically replace underscores with dashes.
