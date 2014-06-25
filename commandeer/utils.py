from re import compile

regex = compile(r'\$(\{[a-zA-Z.]+\}|[a-zA-Z.]+)')

def escape(string):
    return str(string).replace("'", "\\'")

def option_string(positional, options):
    stack = []
    for key, value in options.items():
        string = '{key}'
        if value is not None:
            string = '{key}=\'{value}\''
        string = string.format(key=key, value=escape(value))
        stack.append(string)

    for item in positional:
        stack.append("'{item}'".format(item=escape(item)))
    return ' '.join(stack)

def fetch_value(values, key, default):
    keys = key.split('.')
    for item in keys:
        if item not in values:
            return default
        values = values[item]
    return values

def make_options(options):
    results = {}
    for key, value in options.items():
        key = key.replace('_', '-')
        option = '--{key}'.format(key=key)
        if len(key) == 1:
            option = '-{key}'.format(key=key)
        results[option] = value
    return results
