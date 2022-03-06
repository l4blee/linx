from __future__ import annotations

from vk_api.longpoll import Event

from api import Cog, command
from stages import ButtonLabels, Stages


class Navigation(Cog):
    """
    Navigation commands cog.
    """
    @command(aliases=['настройки'])
    async def settings(self, event: Event):
        stage = Stages.SETTINGS.value
        await self.send_message(user_id=event.user_id,
                                text=stage.msg_text,
                                keyboard=stage.get_keyboard())

    @command(aliases=['домой'])
    async def home(self, event: Event):
        stage = Stages.MAIN.value
        await self.send_message(user_id=event.user_id,
                                text=stage.msg_text,
                                keyboard=stage.get_keyboard())
