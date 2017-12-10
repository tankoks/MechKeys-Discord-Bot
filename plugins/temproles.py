from pluginFramework import pluginShell
from attributes import userCommand
from attributes import backgroundLoop
import asyncio
import discord
import re

import CONFIG

class Verification(pluginShell):
    @userCommand
    async def flashsales(self, message):
        if (
        ("I understand that this channel"
        " will have everyone pings"
        " and that abusing them can result in a ban."
        " I also understand that this channel is a privilege."
        " I am entitled to everything."
        " Sony is a piece of shit."
        " I deserve everything.") in message.content.lower()
        or message.content.lower().startswith("!flashsale")):
            await addTempRole(message, message.author, CONFIG.TEMPROLEIDS["flashsales"])


    #helper function to add temproles
    async def addTempRole(message, member, role):
        for memberroles in message.author.roles:
            if memberroles.id == role:
                roleAdd = discord.utils.get(message.server.roles,
                    id = role)
                await self.clientInstance.remove_roles(message.author, roleAdd)
                await self.clientInstance.delete_message(message)
                return
            else:
                continue
        roleAdd = discord.utils.get(message.server.roles,
            id = role)
        await self.clientInstance.add_roles(message.author, roleAdd)
        await self.clientInstance.delete_message(message)
