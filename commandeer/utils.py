def make_options(options):
    results = {}
    for key, value in options.items():
        key = key.replace('_', '-')
        option = '--{key}'.format(key=key)
        if len(key) == 1:
            option = '-{key}'.format(key=key)
        results[option] = value
    return results
