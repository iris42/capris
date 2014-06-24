from re import compile

regex = compile(r'\$(\{[a-zA-Z]+\}|[a-zA-Z]+)(?=[^\']*(?:\'[^\']*\'[^\']*)*$)')

def substitute_values(string, values, default=''):
    def callback(m):
        key = m.group(1).strip('{').strip('}')
        return values.get(key, default)
    return regex.sub(callback, string)
