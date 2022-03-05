from __future__ import annotations

from vk_api.longpoll import Event

from cogs import Cog, command
from stages import ButtonLabels


class Navigation(Cog):
    """
    Navigation commands cog.
    """
    @command(aliases=['настройки'])
    async def settings(self, event: Event):
        await self.send_message(event.user_id, stage='SETTINGS')

    @command(aliases=['домой'])
    async def home(self, event: Event):
        await self.send_message(event.user_id, stage='MAIN')
