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

## Shell-like substitution

You can perform shell-like substitution on the command string
before you run the command, provided that you explicitly
double quote everything, for example:

```python
echo = Command('echo')
echo('"$value"', n=None)

response = echo.run(values={'value':'Hello!'})
assert response.std_out == 'Hello!'
```
