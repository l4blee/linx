import sys
import asyncio
import logging
from datetime import datetime
from traceback import print_exception

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard

from stages import Stages, ButtonLabels
from commands import Commands
from cogs import Cog, Command


class BotClient(VkApi):
    def __init__(self, mongo_client, **kwargs):
        super().__init__(**kwargs)

        self.mongo_client = mongo_client
        self.longpoll = VkLongPoll(self)
        self.logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__qualname__)

        self.cogs: set = set()

    def register_cog(self, cog: Cog):
        self.cogs.add(cog)
        for cmd in cog.get_commands():
            for name in cmd.aliases:
                setattr(self, name, cmd)
    
    def run(self):
        self.logger.info('Registering cogs...')
        self.register_cog(Commands(self))

        all_cmds = [i for i in dir(self) if isinstance(getattr(self, i), Command)]
        self.logger.info(f'Available commands: {all_cmds}')

        self.logger.info('Starting bot...')
        asyncio.run(self.main())

    async def main(self):
        # TODO: make it asynchronous with asyncio.gather
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and \
                    event.to_me:
                try:
                    await self.on_message(event)
                except Exception as e:
                    await self.on_error(e, event)

    async def on_error(self, exception, event):
        await self.send_message(event.user_id,
                                'Произошла ошибка во время выполнения...',
                                'MAIN')

        self.logger.warning(f'Ignoring exception {type(exception)}: {exception}')
        print_exception(type(exception), exception, exception.__traceback__, file=sys.stderr)

    async def on_message(self, event) -> None:
        try:
            cmd = getattr(self, event.text.lower())
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
    def get_stage(stage):        
        return Stages[stage].value
