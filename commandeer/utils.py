from re import compile
import os

regex = compile(r'\$(\{[a-zA-Z.]+\}|[a-zA-Z.]+)')

def which(executable):
    path = os.getenv('PATH')
    for directory in path.split(os.path.pathsep):
        fpath = os.path.join(directory, executable)
        if os.path.exists(fpath) and os.access(fpath, os.X_OK):
            return fpath
    raise ValueError('executable {name} is not found'.format(name=executable))

def escape(string):
    if string in (True, False):
        return str(string).lower()

    if isinstance(string, int):
        return str(string)
    string = str(string).replace("'", "\\'")\
                        .replace('"', '\\"')
    return "'%s'" % (string)

def option_string(positional, options):
    for key, value in options.items():
        option = ("--{key}" if len(key) > 1 else \
                  "-{key}").format(key=key.replace('_','-'))

        string = ("{option}" if value is None else \
                  "{option} {value}" if len(key) == 1 else \
                  "{option}={value}")
        yield string.format(
                option=option,
                value=escape(value)
                )

    for item in positional:
        yield escape(item)
