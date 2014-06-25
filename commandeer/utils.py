from re import compile
import os

regex = compile(r'\$(\{[a-zA-Z.]+\}|[a-zA-Z.]+)')
optionify = lambda string: string.replace('_', '-')

def which(executable):
    path = os.getenv('PATH')
    for directory in path.split(os.path.pathsep):
        fpath = os.path.join(directory, executable)
        if os.path.exists(fpath) and os.access(fpath, os.X_OK):
            return fpath
    return executable

def escape(string):
    if string in (True, False):
        return str(string).lower()

    if isinstance(string, int):
        return str(string)
    string = str(string).replace("'", "\\'")\
                        .replace('"', '\\"')
    return "'%s'" % (string)

def option_string(positional, options):
    stack = []
    for key, value in options.items():
        key = ("--{key}" if len(key) > 1 else "-{key} ").format(key=optionify(key))

        string = "{key}={value}"
        if len(key) == 2:
            string = '{key} {value}'
        elif value is None:
            string = '{key}'

        string = string.format(
                key=key,
                value=escape(value)
                ).strip()
        stack.append(string)

    for item in positional:
        stack.append(escape(item))
    return ' '.join(stack)

def fetch_value(values, key, default):
    keys = key.split('.')
    for item in keys:
        if item not in values:
            return default
        values = values[item]
    return values
