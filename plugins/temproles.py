from pluginFramework import pluginShell
from attributes import userCommand
from attributes import backgroundLoop
import asyncio
import discord
import re

import CONFIG

class Verification(pluginShell):
    def __init__(self, ClientInstance):
        pluginShell.__init__(self, ClientInstance)

    @userCommand
    async def flashsales(self, message):
        await self.addTempRole(self, message, message.author, CONFIG.TEMPROLEIDS["flashsales"])


    @userCommand
    async def casting(self, message):
        await self.addTempRole(self, message, message.author, CONFIG.TEMPROLEIDS["Casting"])


    #helper function to add temproles
    @staticmethod
    async def addTempRole(self, message, member, role):
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
