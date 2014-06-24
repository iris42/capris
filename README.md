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
