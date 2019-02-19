from pluginFramework import pluginShell
from attributes import userCommand
from attributes import backgroundLoop
from attributes import afterCheck
import asyncio
import discord
import re

import CONFIG

class Verification(pluginShell):
    def __init__(self, ClientInstance):
        pluginShell.__init__(self, ClientInstance)



    @afterCheck
    async def verify(self, message):
        if message.channel.id == CONFIG.VERIFYCHAN:
            if CONFIG.VERIFYPHRASE in message.content.lower():
                roleAdd = discord.utils.get(message.server.roles,
                    id = CONFIG.VERIFYROLEID)
                await self.clientInstance.add_roles(message.author, roleAdd)
            await self.clientInstance.delete_message(message)

    @userCommand
    async def na(self, message):
        await self.addRegionRole(self, message, message.author, CONFIG.REGIONROLEID["NA"])
    @userCommand
    async def aus(self, message):
        await self.addRegionRole(self, message, message.author, CONFIG.REGIONROLEID["AUS"])
    @userCommand
    async def sea(self, message):
        await self.addRegionRole(self, message, message.author, CONFIG.REGIONROLEID["SEA"])
    @userCommand
    async def sa(self, message):
        await self.addRegionRole(self, message, message.author, CONFIG.REGIONROLEID["SA"])
    @userCommand
    async def africa(self, message):
        await self.addRegionRole(self, message, message.author, CONFIG.REGIONROLEID["AFRICA"])
    @userCommand
    async def asia(self, message):
        await self.addRegionRole(self, message, message.author, CONFIG.REGIONROLEID["ASIA"])
    @userCommand
    async def me(self, message):
        await self.addRegionRole(self, message, message.author, CONFIG.REGIONROLEID["ME"])
    @userCommand
    async def eu(self, message):
        await self.addRegionRole(self, message, message.author, CONFIG.REGIONROLEID["EU"])


    #helper function to add roles
    @staticmethod
    async def addRegionRole(self, message, member, roleID):
        if message.channel.id == CONFIG.REGIONROLECHAN:
            rolelist = []
            for memberroles in member.roles:
                rolelist.append(memberroles.id)
            for IDs in CONFIG.REGIONROLEID.values():
                if IDs in rolelist:
                    await self.clientInstance.delete_message(message)
                    return
                else:
                    continue
            roleAdd = discord.utils.get(message.server.roles,
                id = roleID)
            await self.clientInstance.add_roles(member, roleAdd)
            await self.clientInstance.delete_message(message)
