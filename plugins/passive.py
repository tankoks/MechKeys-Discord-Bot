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
            try:
                await asyncio.sleep(5.0)
                await self.clientInstance.delete_message(message)
            except:
                pass
        if ("wtt" in message.content.lower() or
        "wts" in message.content.lower() or
        "wtb" in message.content.lower()):
         #or "h:" in message.content.lower()
         #or "w:" in message.content.lower()
         #or "[h]" in message.content.lower()
         #or "[w]" in message.content.lower()
            try:
                await self.clientInstance.send_message(message.author,
'''
This is a reminder that this discord SHOULD NOT be used as a trading platform.
We have no way of preventing scammers from utilizing this service and we have no way to verify trades or crosscheck the scammer list.
Exercise caution if you do trade with other members of the discord, and remember to always use Paypal "Goods and Services" or equivalent.
Trade with users here at your own risk.
''')
            except:
                pass
