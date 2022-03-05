from __future__ import annotations

from cogs import Cog, command
from stages import ButtonLabels


class Commands(Cog):
    def __init__(self, client: core.BotClient):
        self.client = client

    @command(aliases=['настройки'])
    async def settings(self, event: vk.Event):
        await self.send_message(event.user_id, stage='SETTINGS')
