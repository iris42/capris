# Transactions

Transactions represent blocks of commands that should be
ran in sequence to one another and will continue to be
ran if and only there are no failures. For example:

```python
from capris.transaction import transactional

@transactional()
def setup(transaction):
    make = transaction.make
    make.run()
    make.install.run()
    return transaction

transaction = setup()
results = transaction.execute()
```

All commands gained from the `transaction` object passed
as the first parameter that are `run`-ed in the decorated
function will not be ran until the `Transaction.execute`
method is called.

### `@capris.transaction.transactional(lazy=False)`

A decorator that accepts a single argument, the `lazy`
option and returns a function that will call the decorated
function with a `Transaction` object as the first parameter,
for example:

```python
@transactional()
def setup(transaction):
    print(transaction)

setup()
# <capris.transaction.Transaction object at 0x...>
```

If you set the `lazy` option to `True`, the function
will only be ran if the `defined` property of the
`Transaction` object evaluates to `False`. For
example:

```python
context = []

@transactional(lazy=True)
def setup(transaction):
    context.append(transaction)
    transaction.grep.run()

[setup() for _ in range(2)]
assert len(context) == 1
```


## `capris.transaction.Transaction`

Methods defined on the transaction object:

 - `Transaction.command(string)`
 - `Transaction.execute()`
 - `Transaction.commands`
 - `Transaction.defined`


### `Transaction.command(string)`

An alias would be to use the `getattr` magic, but you
can just do a regular python call if you need dynamism
and that's your thing. Returns a lazy `TransactionCommand`
object that will not run when the `run` method is called.
Example usage:

```python
transaction.command('make')
transaction.make
```

### `Transaction.execute()`

Executes the transaction and runs all of the commands in
the behaviour specified in the beginning of this document.
Returns a list of `capris.core.Response` objects returned
by calling the correct (i.e. `pipes -> Pipe.run`, etc)
runner method on the object. For example:

```python
results = transaction.execute()
for response in results:
    # ...
```

### `Transaction.commands`

A list of commands registered on the transaction object.
You shouldn't manipulate this directly as the data stored
in the list may change in format without prior notice.
The current format is:

```python
(runnable, runner_method, args, kwargs)
```

Essentially when you call the `run` method of runnables
returned by the `transaction.command` method, you are
registering a command to be ran on the transaction
object.

### `Transaction.defined`

A property that determines if a transaction is defined,
or whether there are commands registered (their `run`
method is called) on the transaction. For example:

```python
@transactional()
def setup(transaction):
    if not transaction.defined:
        # continue defining
    return transaction
```
