def escape(value):
    if value in (True, False):
        return str(value).lower()
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


class Command(object):
    base = ()

    def __init__(self, name, *arguments, **options):
        self.command = name
        self.arguments = list(arguments)
        self.options = options

    def __iter__(self):
        for item in self.base:
            yield item

        yield self.command
        for item in self.arguments:
            yield escape(item)

        for item in optionify(self.options):
            yield item

    def subcommand(self, command, arguments=(), options={}):
        cmd = Command(command,
                      *arguments,
                      **options)
        cmd.base = self
        return cmd

    def __call__(self, *arguments, **options):
        self.arguments.extend(arguments)
        self.options.update(options)
        return self

    def __getattr__(self, attribute):
        values = self.__dict__
        if attribute in values:
            return values[attribute]

        attribute = attribute.replace('_', '-')
        return self.subcommand(attribute)
