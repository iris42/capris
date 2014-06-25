commandeer
==========

Commandeer is a library for helping you write apps that use
the command line easily and build up the commands easily as
well, for example to build an easy git wrapper:

```python
from commandeer import Command

git = Command('git')
git.init.run()

commit = git.commit(m="Commit message")
commit.run()
```

Underneath the hood, `commandeer` uses the `envoy` library
to execute the commands and return responses. The `commandeer`
library is nothing more than a command-generator, and all it
does is become a DSL for generating commands:

```python
>>> git = Command('git')
>>> str(git.log(graph=None, date="relative"))
'git log --graph --date="relative"'
```

Note that when you create call subcommand or call a command
object with braces i.e. `git()`, you will get a _copy_ of
the command object with updated options and positional arguments.
For example:

```python
>>> git = Command('git')
>>> git(bare=None) is git
False
>>> git.log() is git.log()
False
```

## Piping Commands

You can pipe commands using the `Pipe` class, for example the
trivial case of listing the directory and then `grep`-ing for
a particular pattern on the output:

```python
from commandeer import Command, Pipe
pipe = Pipe()
pipe += Command('ls')
pipe += Command('grep', '.py')

response = pipe.run()
for filename in response.std_out.strip().split('\n'):
    print(filename)
```

Also, instead of manually building up the pipe object, you can
also use a more convenient method of using the `or` operator
on the command/pipe objects:

```python
pipe = git.log(date='relative') | grep('name')
response = pipe.run()
```

## Timeouts, and passing data to stdin

You can pass the `timeout` and `data` keyword arguments (respectively)
to limit the execution time and pass in data to stdin. For
example to pass some data to `grep`:

```python
grep = Command('grep')
response = grep('pattern').run(data='pattern pattern')
print(response.std_out.strip())
# => 'pattern pattern'
```

All other keyword arguments that are supported by the `envoy.run`
function will also be accepted here, because the `Command.run`
function delegates these keyword arguments to the `envoy.run`
function.

## Redirection

Redirection is very simple, if you want to do it with a bit of
syntactic sugar. For example to `grep` a pattern from a file
that has been read into memory we can do:

```python
import sys
grep = Command('grep')

iostream = open('setup.py') > grep('import *').iostream > sys.stdout
response = iostream.run()
```

The reason that we need to do the `.iostream` is because we
need to ensure some _correctness_- for example a command that
has been redirected shouldn't affect the main command object
but instead return a new command object, or at least a `run`-able
object.

You can also pipe `IOContext` objects (those obtained from
the `iostream` attribute of pipes or commands just like
you would normally do to pipes or commands, for example:

```python
>>> pipe = python('commits.py') | grep('[a-e0-9]\{40\}').iostream
>>> str(pipe)
"python 'commits.py' | grep '[a-e0-9]\\{40\\}'"
```
