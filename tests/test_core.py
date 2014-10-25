from capris.core import run
from capris.utils import optionify


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


def test_optionify():
    options = {'items': 1, 'this': None}
    flags = {'i': 'o', 'z': None}

    assert set(optionify(options)) == set(['--items=1', '--this'])
    assert set(optionify(flags)) == set(['-i=o', '-z'])
