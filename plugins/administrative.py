from pluginFramework import pluginShell
from attributes import userCommand
from attributes import backgroundLoop
from attributes import afterCheck
import asyncio
import discord
import re
import json
import requests
import os


import CONFIG



class Administrative(pluginShell):

    @userCommand
    async def purge(self, message):
        mods = discord.utils.get(
            message.server.roles, id = CONFIG.MODS_ID)
        mod2 = mods = discord.utils.get(
            message.server.roles, id = CONFIG.MOD2_ID)
        if mods in message.author.roles or mod2 in message.author.roles:
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

    @afterCheck            
    async def on_message(self, message):
        if len(message.attachments) >= 0:
            attachments = message.attachments
            sendChannel = discord.utils.get(self.clientInstance.get_all_channels(),
                id = "FIXME_CHANNELID")
            
            for x in range(len(attachments)):
                attachment = attachments[x]
                try:
                    await self.clientInstance.send_message(sendChannel, attachment['url'])
                except Exception as e:
                    print(e)
                    pass


    async def on_message_delete(self, message):
        if (message.author != self.clientInstance.user
            and message.channel.id != CONFIG.VERIFYCHAN
            and message.channel.id != CONFIG.REGIONROLECHAN
            and not message.content.startswith("!lifealert")
            and not message.content.startswith("!callamod")):

            sendChannel = discord.utils.get(self.clientInstance.get_all_channels(),
                id = "FIXME_CHANNELID")

            embed = discord.Embed(
                title="Message Deleted",
                color=0xff0000)
            embed.add_field(name="User", value=message.author.name + "#" + message.author.discriminator, inline = True)
            embed.add_field(name="ID", value=message.author.id, inline = True)
            embed.add_field(name="Channel", value=message.channel.mention, inline = False)
            embed.add_field(name="Time", value=message.timestamp.isoformat(), inline = True)
            if message.clean_content:
                embed.add_field(name="Message", value=message.clean_content, inline = False)
            await self.clientInstance.send_message(sendChannel, embed=embed)
            
            attachments = message.attachments
            
            for x in range(len(attachments)):
                attachment = attachments[x]
                try:
                    response = requests.get(attachment["url"], allow_redirects=False)
                    filename = attachment["url"].split("/")[-1]
                    open(filename,'wb').write(response.content)

                    await self.clientInstance.send_file(sendChannel, fp=filename, content="Deleted Content: " + str(x+1))
                    os.remove(filename)
                except Exception as e:
                    print(e)
                    pass

    async def on_message_edit(self, message, after):
        if (message.author != self.clientInstance.user
        and message.channel.id != CONFIG.VERIFYCHAN
        and message.channel.id != CONFIG.REGIONROLECHAN
	and not message.channel.is_private
        and not message.content.startswith("!lifealert")
        and not message.content.startswith("!callamod")
        and message.clean_content != after.clean_content):
            sendChannel = discord.utils.get(self.clientInstance.get_all_channels(),
                id = "FIXME_CHANNELID")

            embed = discord.Embed(
                title="Message Edited",
                color=0x0000ff)
            
            embed.add_field(name="User", value=message.author.name + "#" + message.author.discriminator, inline = True)
            embed.add_field(name="ID", value=message.author.id, inline = True)
            embed.add_field(name="Channel", value=message.channel.mention, inline = False)
            embed.add_field(name="Time Edited", value=message.timestamp.isoformat(), inline = True)
            if after.clean_content:
                embed.add_field(name="Previous Message", value=message.clean_content, inline = False)
            if message.clean_content:
                embed.add_field(name="New Message", value=after.clean_content, inline = False)
            await self.clientInstance.send_message(sendChannel, embed=embed)

            attachments = message.attachments
            
            for x in range(len(attachments)):
                attachment = attachments[x]
                try:
                    response = requests.get(attachment["url"], allow_redirects=False)
                    filename = attachment["url"].split("/")[-1]
                    open(filename,'wb').write(response.content)

                    await self.clientInstance.send_file(sendChannel, fp=filename, content="Deleted Content: " + str(x+1))
                    os.remove(filename)
                except Exception as e:
                    print(e)
                    pass
