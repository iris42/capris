# Commandeer

`commandeer` is a DSL for creating beautiful apps that leverage
the command line in Python. `commandeer` purely generates commands
and does not handle the running of commands- that is the job of
the `envoy` library. A simple example of `commandeer` at work:

```python
from commandeer import *
git = Command('git')
grep = Command('grep')

pipe = git.log(graph=None) | grep('commit: [a-f0-9]\{40\}')
response = pipe.run()
```

There are three base classes in `commandeer`- `Command`, `Pipe`,
and `IOContext`. If you are not piping commands or doing
redirection you are most likely to just use the `Command`
class.

## `commandeer.command.Command`

A `Command` object represents a single command which can be
chained to create readable subcommands. It only has a few
methods and inherits from the base `Runnable` class:

 - `Command.options_string`
 - `Command.copy`
 - `Command.subcommand`

### `Command.options_string`

A property that transforms the positional arguments and
options of a command into a string, placing the options
before the arguments unix-style. For example:

```python
>>> command.options_string
"-n --option='string'"
```

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
