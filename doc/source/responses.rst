Responses
=========

Responses are units of data in **Capris** that represent
the stdout, stderr, exit code, environment, history, and
exception that running command used/raised. In short, they
are encapsulation around several components.

You will get responses if you run non-transactional runnables
using their ``run`` method. For the rest of this documentation
I will use run instead of "call the ``run`` method" where
suitable. An example of a response::

    >>> res = git.log(n=10).run()
    >>> res.ok()
    True

Exit Codes
----------

To check the exit code of a command you need to use the
``status_code`` attribute. For example::

    >>> res = r.run()
    >>> res.status_code
    0

However, keep in mind that if the runnable is either a
pipe or an iostream object the exit code of the response
object will only give you the exit code of the `last`
command ran. For example, if you did the following::

    >>> r = git.log(n=10, pretty="format:%m") | grep('message')
    >>> res = r.run()

The ``status_code`` of your ``res`` variable will be that
of ``grep``, not ``git``. To access that of ``git`` you
will have to look into the history of the response object.


Command History
---------------

The history of a response stores the previously ran
commands prior to the last command (the one which the
current response object represents). This attribute
is only set in the last command, prehaps best illustrated
with an example::

    >>> res = pipe.run()
    >>> res.history
    [<Response [git]>, <Response [grep]>]
    >>> res.history[-1].history
    []

If you run pipes or iostreams for pipes, you should
get the above if the pipe contains more than one
command. The validity of the history is not enforced
by the response object, i.e. you can append to it and
modify it as you like.


Standard Output and Error
-------------------------

To access the standard output of the command, as well
as the contents of stderr streams you can use the
``std_out`` and ``std_err`` attribtues respectively.
For a simple example::

    >>> res = echo('message').run()
    >>> res.std_out
    'message\n'
    >>> res.std_err
    ''
