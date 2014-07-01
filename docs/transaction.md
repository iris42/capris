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

The above example is what the `&&` operator does in the
POSIX shells, that is that it will execute the next
command if the previous is succesful. All commands gained
from the `transaction` object passed as the first parameter
that are `run`-ed in the transactional method will not be
ran until the `Transaction.execute` method is called.
Methods defined on the transaction object:

 - `Transaction.command(string)`
 - `Transaction.execute()`
 - `Transaction.commands`
 - `Transaction.defined`


## `Transaction.command(string)`

An alias would be to use the `getattr` magic, but you
can just do a regular python call if you need dynamism
and that's your thing. Returns a lazy `TransactionCommand`
object that will not run when the `run` method is called.
Example usage:

```python
transaction.command('make')
transaction.make
```

## `Transaction.execute()`

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

## `Transaction.commands`

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

## `Transaction.defined`

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
