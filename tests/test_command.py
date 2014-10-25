from capris.commons import cat, echo, grep


def test_basic():
    assert echo('haha').run().stdout == 'haha\n'
    assert echo('this').run().ok()


def test_environ():
    this = echo.this
    that = this.that

    this.env = {
        'something': 1,
        'some': 1,
    }
    that.env['something'] = 2

    assert that.environ['some'] == 1
    assert this.environ['something'] == 1
    assert that.environ['something'] == 2


def test_data():
    r = cat.run(data='this')
    assert r.ok()
    assert r.stdout == 'this'


def test_options_before_args():
    r = grep(20, n=10)
    assert list(r) == ['grep', '-n=10', '20']
