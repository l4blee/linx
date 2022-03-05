import sys
import asyncio
import logging
from datetime import datetime
from traceback import print_exception
from json import loads

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.keyboard import VkKeyboard

from stages import Stages, ButtonLabels
from commands import Navigation
from cogs import Cog, Command, CommandPool


class BotClient(VkApi):
    def __init__(self, mongo_client, **kwargs):
        super().__init__(**kwargs)

        self.mongo_client = mongo_client
        self.longpoll = VkLongPoll(self)
        self.logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__qualname__)

        self.cogs: set = set()
        self.command_pool: CommandPool = CommandPool()

    def register_cog(self, cog: Cog) -> None:
        self.cogs.add(cog)
        self.command_pool.register_cog(cog)
    
    def run(self) -> None:
        self.logger.info('Registering cogs...')

        # Registering cogs(manually)
        self.register_cog(Navigation())

        self.logger.info(f'Available commands: {self.command_pool.to_list()}')

        self.logger.info('Starting bot...')
        asyncio.run(self.main())

    async def main(self) -> None:
        # TODO: make it asynchronous with asyncio.gather
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and \
                    event.to_me:
                try:
                    await self.on_message(event)
                except Exception as e:
                    await self.on_error(e, event)

    async def on_error(self, exception: Exception, event: Event) -> None:
        await self.send_message(event.user_id,
                                'Произошла ошибка во время выполнения...',
                                'MAIN')

        self.logger.warning(f'Ignoring exception {type(exception)}: {exception}')
        print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    @staticmethod
    def recv_cmd_from_payload(event: Event):
        if (payload := event.raw[6].get('payload')):
            # Since basically payload is represented as an str
            return loads(payload).get('command')

    async def on_message(self, event: Event) -> None:
        try:
            payload_cmd = self.recv_cmd_from_payload(event)
            if payload_cmd:
                cmd = getattr(self.command_pool, payload_cmd)
            else:
                cmd = getattr(self.command_pool, event.text)
        except AttributeError:
                await self.send_message(event.user_id,
                                        'Такой команды нет, попробуйте еще раз!')
                return

        await cmd(self, event)

    async def send_message(self, user_id: int, text: str = None, stage: str = None) -> None:
        stage = self.get_stage(stage or 'MAIN')

        self.method(
            'messages.send',
            {
                'user_id': user_id,
                'random_id': self.generate_random_id(),
                'keyboard': stage.get_keyboard(),
                'message': text or stage.msg_text
            }
        )

    @staticmethod
    def generate_random_id() -> int:
        return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def get_stage(stage) -> Stages:        
        return Stages[stage].value
