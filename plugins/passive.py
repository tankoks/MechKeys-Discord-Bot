from pluginFramework import pluginShell
from attributes import userCommand
from attributes import backgroundLoop
from attributes import afterCheck
import asyncio
import discord
import re

import CONFIG

class Passive(pluginShell):

    @afterCheck
    async def autoDelete(self, message):
        if (message.channel.id == CONFIG.VERIFYCHAN or
            message.channel.id == CONFIG.REGIONROLECHAN):
            await self.clientInstance.delete_message(message)
