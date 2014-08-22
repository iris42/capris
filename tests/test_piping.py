from capris.command import Command


echo = Command('echo')
cat = Command('cat')


def test_piping():
    pipe = echo('haha') | cat
    response = pipe.run()

    assert response.ok()
    assert response.command == ('cat',)
    assert response.stdout == 'haha\n'
    assert response.history[0].command == ('echo', 'haha')


def test_compound_pipe():
    pipe = (echo('haha') | cat) | (cat | cat)
    response = pipe.run()

    assert response.ok()
    assert response.stdout == 'haha\n'


def test_pipe_pipes():
    pipe1 = echo('haha') | cat
    pipe2 = pipe1 | cat
    response = pipe2.run()

    assert response.ok()
    assert response.stdout == 'haha\n'
