from pluginFramework import pluginShell
from attributes import userCommand
from attributes import backgroundLoop
import asyncio
import discord
import re

import CONFIG

class Verification(pluginShell):
    @userCommand
    async def verify(self, message):
        if message.channel.id == CONFIG.VERIFYCHAN:
            if message.contents.lower = CONFIG.VERIFYPHRASE
                roleAdd = discord.utils.get(message.server.roles,
                    id = CONFIG.VERIFYROLEID)
                await self.clientInstance.add_roles(message.author, roleAdd)
            await self.clientInstance.delete_message(message)

    @userCommand
    async def NA(self, message):
        await addRegionRole(message, message.author, CONFIG.REGIONROLEID["NA"])
    @userCommand
    async def AUS(self, message):
        await addRegionRole(message, message.author, CONFIG.REGIONROLEID["AUS"])
    @userCommand
    async def SEA(self, message):
        await addRegionRole(message, message.author, CONFIG.REGIONROLEID["SEA"])
    @userCommand
    async def SA(self, message):
        await addRegionRole(message, message.author, CONFIG.REGIONROLEID["SA"])
    @userCommand
    async def AFRICA(self, message):
        await addRegionRole(message, message.author, CONFIG.REGIONROLEID["AFRICA"])
    @userCommand
    async def ASIA(self, message):
        await addRegionRole(message, message.author, CONFIG.REGIONROLEID["ASIA"])
    @userCommand
    async def ME(self, message):
        await addRegionRole(message, message.author, CONFIG.REGIONROLEID["ME"])


    #helper function to add roles
    async def addRegionRole(message, member, roleID):
        if message.channel.id == CONFIG.REGIONROLECHAN:
            rolelist = []
            for memberroles in member.roles:
                rolelist.append(memberroles.id)
            for IDs in roleIDs:
                if IDs in rolelist:
                    await self.clientInstance.delete_message(message)
                    return
                else:
                    continue
            roleAdd = discord.utils.get(message.server.roles,
                id = roleID)
            await self.clientInstance.add_roles(member, roleAdd)
            await self.clientInstance.delete_message(message)
