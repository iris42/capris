def escape(value):
    if value is True or value is False:
        return 'true' if value else 'false'
    return str(value)


def optionify(options):
    for key, value in options.items():
        key = key.replace('_', '-')
        is_flag = len(key) == 1
        if value is None:
            yield ('-%s' if is_flag else '--%s') % key
            continue
        yield ('-%s=%s' if is_flag else
               '--%s=%s') % (key, escape(value))
