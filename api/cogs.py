from typing import Coroutine


class Command:
    """
    Command representative for cogs' methods.
    Should always be called with CMD_NAME(client, event) to
    reach behaviour as if it was a client's method.
    """
    def __init__(self, callback, aliases=None):
        self.calllback = callback
        self.aliases = (aliases or []) + [callback.__name__]
    
    def __call__(self, client, event) -> Coroutine:
        return self.calllback(client, event)


class Cog:
    def get_commands(self) -> list[Command]:
        methods = [getattr(self, i) for i in dir(self)]
        return [i for i in methods if isinstance(i, Command)]

class CommandPool:
    """
    Used as a internal storage of all the commands in order to not use
    cmds as attributes of a main class.
    """
    def register_cog(self, cog: Cog) -> None:
        if not isinstance(cog, Cog):
            raise TypeError('Cogs must be inherited from the Cog class.')

        for cmd in cog.get_commands():
            for name in cmd.aliases:
                setattr(self, name, cmd)

    def to_list(self) -> list[str]:
        return [attr_name
                for attr_name in dir(self)
                if isinstance(getattr(self, attr_name), Command)]


def command(aliases: list = None):
    """
    A decorator for registering cogs' commands via
    tranforming them into Command class.
    """
    aliases = aliases or []

    def wrapper(function):
        if isinstance(function, Command):
            raise TypeError('Callback is already a command.')
        return Command(function, aliases=aliases)
        
    return wrapper