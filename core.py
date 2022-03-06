import json
from importlib import import_module
from pathlib import Path 

from vk_api.longpoll import Event

from api import Bot

from stages import Stages


class Client(Bot):
    def __init__(self, mongo_client, **kwargs):
        super().__init__(**kwargs)

        self.mongo_client = mongo_client

    def setup(self) -> None:
        self.logger.info('Registering cogs...')

        for cls in [
            import_module(f'cogs.{i.stem}').__dict__[i.stem.title()]
            for i in Path('cogs/').glob('*.py')
        ]:
            self.register_cog(eval('cls()'))

    @staticmethod
    def parse_cmd(event: Event) -> str:  # Returns payload cmd name
        if (payload := event.raw[6].get('payload')):
            # Since basically payload is represented as an str
            return json.loads(payload).get('command')
    
    async def on_message(self, event: Event) -> None:
        try:
            cmd = self.parse_cmd(event)
            if cmd is not None:
                callback = getattr(self.command_pool, cmd)
            else:
                callback = getattr(self.command_pool, event.text)
        except AttributeError:
            await self.send_message(user_id=event.user_id,
                                    text='Такой команды нет, попробуйте еще раз!',
                                    keyboard=Stages.MAIN.value.get_keyboard())
            return

        await callback(self, event)