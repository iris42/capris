capris
======

Capris is a wrapper around the subprocess library for easily writing
beautiful applications that leverage the command line.

.. code-block:: python

    from capris import Command
    git = Command('git')

    response = git.log(n=10).run()
    assert response.ok()

It can be used (and is most suited) for testing command line tools
as well. Combining it with the ``assert`` statement makes for very
nice and elegant code.
