from cProfile import runctx
from capris import Command, Pipe
from capris.core import run, run_command

PROFILED = []


def profiled(fn):
    def wrapper():
        runctx('fn()', {}, {'fn':fn})
    wrapper.func = fn
    PROFILED.append(wrapper)
    return fn


@profiled
def profile_run_command():
    response = run_command(['env'])


@profiled
def profile_run():
    response = run([['echo', 'pattern'], ['grep', 'pattern']])


if __name__ == "__main__":
    for item in PROFILED:
        print(item.func.__name__)
        item()
