import asyncio
import logging
from datetime import datetime

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard

from stages import Stages, ButtonLabels


class BotClient(VkApi):
    def __init__(self, mongo_client, **kwargs):
        super().__init__(**kwargs)

        self.mongo_client = mongo_client
        self.longpoll = VkLongPoll(self)
        self.logger = logging.getLogger(self.__class__.__module__ + '.' + self.__class__.__qualname__)
    
    def run(self):
        self.logger.info('Starting bot...')
        asyncio.run(self.main())

    async def main(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and \
                    event.to_me:
                await self.on_message(event)

    async def on_message(self, event) -> None:
        self.logger.debug(f'Got a message from {event.user_id}, processing...')

        if event.text == ButtonLabels.SETTINGS:
            await self.send_message(event.user_id, event.text, 'SETTINGS')
        elif event.text == ButtonLabels.BACK:
            await self.send_message(event.user_id, event.text, 'MAIN')
        else:
            await self.send_message(event.user_id, event.text)

    async def send_message(self, user_id: int, text: str, stage: str = None) -> None:
        stage = stage or 'MAIN'
        stage = self.get_stage(stage)

        self.method(
            'messages.send',
            {
                'user_id': user_id,
                'random_id': self.generate_random_id(),
                'keyboard': stage.get_keyboard(),
                'message': stage.msg_text
            }
        )

    @staticmethod
    def generate_random_id() -> int:
        return int(datetime.now().timestamp() * 1000)

    @staticmethod
    def get_stage(stage):        
        return Stages[stage].value
