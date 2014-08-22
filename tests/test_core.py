from capris.core import run


def test_run():
    commands = [
        [['echo', 'this']],
        [['echo', 'this'], ['cat']],
    ]
    for index, item in enumerate(commands):
        r = run(item)
        assert r.ok()
        assert r.stdout == 'this\n'
        if index:
            assert r.history
            assert r.history[0].command == ['echo', 'this']
