class Command:
    def __init__(self, callback, aliases=None):
        self.callback = callback
        self.aliases = (aliases or []) + [callback.__name__]
        self.cog = None

    def __call__(self, *args, **kwargs):
        return self.callback(*args, **kwargs)

def command(aliases: list = None):
    aliases = aliases or []
    def wrapper(func):
        return Command(func, aliases=aliases)
    return wrapper


class Cog:
    def get_commands(self):
        methods = [getattr(self, i) for i in dir(self)]
        return [i for i in methods if isinstance(i, Command)]
