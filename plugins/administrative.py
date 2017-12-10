from pluginFramework import pluginShell
from attributes import userCommand
from attributes import backgroundLoop
import asyncio
import discord
import re

import CONFIG

class Administrative(pluginShell):

    @userCommand
    async def purge(self, message):
        mods = discord.utils.get(
            message.server.roles, id = CONFIG.MODS_ID)
        if mods in message.author.roles:
            num = re.sub(r'\D', '', message.content)
            if num != "":
                await self.clientInstance.purge_from(message.channel,
                    limit = int(num))
            else:
                def intCheck(msg):
                    return msg.content.isdigit()

                await self.clientInstance.send_message(message.channel,
                    'Purge how many messages?')
                purgeNum = await self.clientInstance.wait_for_message(timeout=100.0,
                    author = message.author, check = intCheck)
                await self.clientInstance.purge_from(message.channel,
                    limit = int(purgeNum.content))
