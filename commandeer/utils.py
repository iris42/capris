from re import compile

regex = compile(r'\$(\{[a-zA-Z.]+\}|[a-zA-Z.]+)(?=[^\']*(?:\'[^\']*\'[^\']*)*$)')

def substitute_values(string, values, default=''):
    def callback(m):
        key = m.group(1).strip('{').strip('}')
        return fetch_value(values, key, default)
    return regex.sub(callback, string)

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
