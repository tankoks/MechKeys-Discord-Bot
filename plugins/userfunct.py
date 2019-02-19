from pluginFramework import pluginShell
from attributes import userCommand
from attributes import backgroundLoop
import asyncio
import discord
import re

import CONFIG

class UserFunct(pluginShell):

    @userCommand
    async def vote(self, message):
        await self.clientInstance.add_reaction(message,"👍")
        await self.clientInstance.add_reaction(message,"👎")

    @userCommand
    async def lifealert(self, message):
        sendChannel = discord.utils.get(self.clientInstance.get_all_channels(),
                id = "325265301958557696")
        await self.clientInstance.send_message(sendChannel,
                "MODMESSAGE from {}#{} at {} in {}. Message was ``` {} ``` with attachments {}".format(
                    message.author.name, message.author.discriminator, message.timestamp.isoformat(), message.channel.mention, message.clean_content, message.attachments))
        await self.clientInstance.delete_message(message)

    @userCommand
    async def callamod(self, message):
        await self.lifealert(message)

    @userCommand
    async def trade(self, message):
        await self.clientInstance.send_message(message.channel,
'''
This is a reminder that this discord SHOULD NOT be used as a trading platform.
We have no way of preventing scammers from utilizing this service and we have no way to verify trades or crosscheck the scammer list.
Exercise caution if you do trade with other members of the discord, and remember to always use Paypal "Goods and Services" or equivalent.
Trade with users here at your own risk.
''')
