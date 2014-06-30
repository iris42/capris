import os

def which(executable):
    if os.path.exists(executable):
        return os.path.abspath(executable)

    path = os.getenv('PATH') or os.defpath

    for directory in path.split(os.pathsep):
        fpath = os.path.join(directory, executable)
        if os.path.exists(fpath) and os.access(fpath, os.X_OK):
            return fpath
    raise RuntimeError('executable {name} is not found'.format(name=executable))

def escape(string):
    if string in (True, False):
        return str(string).lower()
    return str(string)

def option_iterable(positional, options):
    for key, value in options.items():
        is_argument = len(key) == 1
        option = ("-%s" if is_argument else \
                  "--%s") % key.replace('_', '-')

        if value is None:
            yield option
            continue
        string = "%s %s" if is_argument else \
                 "%s=%s"
        yield string % (option, escape(value))

    for item in positional:
        yield escape(item)
