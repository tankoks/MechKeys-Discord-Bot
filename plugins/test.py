from pluginFramework import pluginShell
from attributes import userCommand
from attributes import backgroundLoop
import asyncio
import discord

class Test(pluginShell):

    @userCommand
    async def test(self, message):
        await self.clientInstance.send_message(message.channel, message.content)


    @backgroundLoop
    async def test2(self):
        while True:
            await asyncio.sleep(5)
