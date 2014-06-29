# Transactions

Transactions represent a series of commands that can be
ran in sequence, and will be executed as far as one
runnable doesn't fail, sort of like a `Makefile`. For
example:

```python
from capris.transaction import Transaction
transaction = Transaction()

with transaction:
    git = transaction.git
    grep = transaction.grep
    if condition:
        transaction.abort()

    pipe = git.log(graph=None) | grep('commit *', o=None)
    pipe.run()

    transaction.execute()
    assert transaction.results[0].status_code == 0
```

When you abort a transaction, the block will still continue
execution but commands added either previously or in the
future will not be executed and the transaction history
will be cleared.

 - `Transaction.lock`
 - `Transaction.abort`
 - `Transaction.execute`
 - `Transaction.results`
 - `Transaction.history`

### `Transaction.lock`

A boolean dictating if the transaction should allow any more
commands added to itself. It will be set when the `transaction.abort`
method is called, and cleared at block entry.

### `Transaction.abort()`

Aborts a transaction and all commands defined earlier or in
the future will not take action. Should be used in situations
where for example you want to run a series of commands if all
conditions are met.

### `Transaction.execute()`

Executes the transaction. The `execute` method will only run
sequential commands as long as the previous command succeeds,
and you must call it to execute your commands within the `with`
block.

```python
for item in self.history:
    response = item.run()
    self.results.append(response)
    if response.status_code != 0:
        break
```

### `Transaction.results`

An attribute that contains the responses from each of the commands
of the last transaction. It is automatically cleared at block entry
and exit.

### `Transaction.history`

A list of commands or runnables, a runner method, and positional and
keyword arguments in an internal format that should all be executed
when the `execute` method is called. If you need to iterate through
all the commands you should do:

```python
for command, _,_,_ in transaction.history:
    # do something
```

It will be cleared on block exit and entry.
