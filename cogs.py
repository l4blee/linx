from abc import abstractclassmethod


class Command:
    """
    Commands should always be called as CMD_NAME(client, event) in order to 
    reach behaviour as if they were client's class attributes
    """
    def __init__(self, callback, aliases=None):
        self.callback = callback
        self.aliases = (aliases or []) + [callback.__name__]

    def __call__(self, client, event):
        return self.callback(client, event)

def command(aliases: list = None):
    aliases = aliases or []

    def wrapper(func):
        return Command(func, aliases=aliases)

    return wrapper


class Cog:
    def get_commands(self):
        methods = [getattr(self, i) for i in dir(self)]
        return [i for i in methods if isinstance(i, Command)]


class CommandPool:
    """
    Used as a internal storage of all the commands in order to not use
    cmds as attributes of a main class.
    """
    def register_cog(self, cog: Cog):
        for cmd in cog.get_commands():
            for name in cmd.aliases:
                setattr(self, name, cmd)

    def to_list(self):
        # Need names, not methods/functions as in Cog.get_commands
        return [i for i in dir(self) if isinstance(getattr(self, i), Command)]
