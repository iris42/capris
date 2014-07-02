import os

__all__ = ['which', 'escape', 'option_iterable']


def which(executable, path):
    if path:
        executable = os.path.join(path, executable)

    if os.path.exists(executable):
        return os.path.abspath(executable)

    path = os.getenv('PATH') if path is None else path

    for directory in path.split(os.pathsep):
        fpath = os.path.join(directory, executable)
        if os.path.exists(fpath) and os.access(fpath, os.X_OK):
            return fpath
    raise RuntimeError('executable %s is not found' % (executable))


def escape(string):
    if string in (True, False):
        return str(string).lower()
    return str(string)


def option_iterable(positional, options):
    for key, value in options.items():
        is_argument = len(key) == 1
        option = ("-%s" if is_argument else
                  "--%s") % key.replace('_', '-')

        if value is None:
            yield option
            continue
        string = ("%s %s" if is_argument else
                  "%s=%s")
        yield string % (option, escape(value))

    for item in positional:
        yield escape(item)
