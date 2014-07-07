from cProfile import run as profile
from capris.core import run, run_command

profile('run_command(["echo", "pattern"])')
profile('run([["grep", "pattern"], ["cat"]], data="pattern")')
