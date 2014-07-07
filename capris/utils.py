from os import getenv, X_OK, access, pathsep
from os.path import join, abspath, exists

__all__ = ['which', 'escape', 'option_iterable']


def which(executable, path):
    if exists(executable):
        return abspath(executable)

    path = getenv('PATH') if path is None else path

    for directory in path.split(pathsep):
        fpath = join(directory, executable)
        if exists(fpath) and access(fpath, X_OK):
            return fpath
    raise RuntimeError('executable %s is not found' % (executable))


def escape(string):
    if string in (True, False):
        return str(string).lower()
    return str(string)


def option_iterable(positional, options):
    for key, value in options.items():
        is_flag = len(key) == 1
        option = ("-%s" if is_flag else
                  "--%s") % key.replace('_', '-')

        if value is None:
            yield option
            continue
        string = ("%s %s" if is_flag else
                  "%s=%s")
        yield string % (option, escape(value))

    for item in positional:
        yield escape(item)
