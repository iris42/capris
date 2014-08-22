from capris.commons import cat, echo


def test_piping():
    pipe = echo('haha') | cat
    r = pipe.run()

    assert r.ok()
    assert r.command == ('cat',)
    assert r.stdout == 'haha\n'
    assert r.history[0].command == ('echo', 'haha')


def test_compound_pipe():
    pipe = (echo('haha') | cat) | (cat | cat)
    r = pipe.run()

    assert r.ok()
    assert r.stdout == 'haha\n'


def test_pipe_pipes():
    pipe1 = echo('haha') | cat
    pipe2 = pipe1 | cat
    r = pipe2.run()

    assert r.ok()
    assert r.stdout == 'haha\n'


def test_iter():
    pipe = echo('haha') | (cat | cat)
    assert list(pipe) == [
        ('echo', 'haha'),
        ('cat',),
        ('cat',),
    ]
