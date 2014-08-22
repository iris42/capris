try:
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
from capris.command import Command

cat = Command('cat')


def test_defaults():
    f_in = StringIO('hello')

    iostream = f_in > cat.iostream
    response = iostream.run(data='this')

    assert response.stdout == 'this'


def test_stringio():
    f_in = StringIO('hello world')
    f_out = StringIO()

    iostream = f_in > cat.iostream > f_out
    response = iostream.run()

    assert response.stdout == 'hello world'
    assert f_out.getvalue() == 'hello world'
