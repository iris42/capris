try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
from capris.commons import cat


def test_defaults():
    f_in = StringIO('hello')

    iostream = f_in > cat.iostream
    r = iostream.run(data='this')

    assert r.stdout == 'this'


def test_stringio():
    f_in = StringIO('hello world')
    f_out = StringIO()

    iostream = f_in > cat.iostream > f_out
    r = iostream.run()

    assert r.stdout == 'hello world'
    assert f_out.getvalue() == 'hello world'


def test_pipe_and_iostream():
    f_in = StringIO('hello world')

    iostream = f_in > (cat | cat).iostream
    r = iostream.run()

    assert r.ok()
    assert r.stdout == 'hello world'
