import sys
import asyncio
import logging
from datetime import datetime
from traceback import print_exception

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.keyboard import VkKeyboard

from . import Cog, CommandPool


class Bot(VkApi):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.longpoll = VkLongPoll(self)
        self.logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__qualname__)

        self.cogs: set = set()
        self.command_pool: CommandPool = CommandPool()

    def setup(self) -> None:
        ...

    def run(self) -> None:
        self.setup()
        self.logger.info(f'Available commands: {self.command_pool.to_list()}')

        self.logger.info('Starting bot...')
        asyncio.run(self.loop())

    async def loop(self) -> None:
        for event in self.longpoll.listen():
            if event.to_me and event.type == VkEventType.MESSAGE_NEW:
                try:
                    await self.on_message(event)
                except Exception as e:
                    await self.on_error(e, event)
    
    async def on_error(self, exception: Exception, event: Event) -> None:
        await self.send_message(event.user_id,
                                'Произошла ошибка во время выполнения...')

        self.logger.warning(f'Ignoring exception {type(exception)}: {exception}')
        print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    async def on_message(self, event: Event) -> None:
        raise NotImplementedError('on_message method must always be implemented')

    async def send_message(self, user_id: int, text: str, keyboard: dict = None) -> None:
        keyboard = keyboard or VkKeyboard.get_empty_keyboard()

        self.method(
            'messages.send',
            {
                'user_id': user_id,
                'message': text,
                'keyboard': keyboard,
                'random_id': self.generate_random_id()
            }
        )

    @staticmethod
    def generate_random_id() -> int:
        return int(datetime.now().timestamp() * 1000)

    def register_cog(self, cog: Cog) -> None:
        if not isinstance(cog, Cog):
            raise TypeError('Cogs must be inherited from the Cog class.')

        self.cogs.add(cog)
        self.command_pool.register_cog(cog)
