# -*- coding: utf-8 -*-
import discord
import asyncio
import time
import random
import datetime
import pickle
import re
import inspect

import CONFIG

#import pluginframework
from pluginFramework import pluginShell as plugins
#import plugins
from plugins.test import *
from plugins.administrative import *
from plugins.raffles import *
from plugins.temproles import *
from plugins.administrative import *
from plugins.passive import *
from plugins.special import *
#from plugins.logs import *


client = discord.Client()
@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



#Function to load all plugins.
loadedPlugins = []
def loadAllPlugins():
    for x in plugins.__subclasses__():
        pluginInstance = x(client)
        loadedPlugins.append(pluginInstance)
loadAllPlugins()


#creates loops to check for client events across all plugins
@client.event
async def on_message(message):
    for x in loadedPlugins:
        client.loop.create_task(x._on_message(message))

@client.event
async def on_message_edit(before, after):
    for x in loadedPlugins:
        client.loop.create_task(x.on_message_edit(before, after))
@client.event
async def on_message_delete(message):
    for x in loadedPlugins:
        client.loop.create_task(x.on_message_delete(message))
@client.event
async def on_channel_create(channel):
    for x in loadedPlugins:
        client.loop.create_task(x.on_channel_create(channel))
@client.event
async def on_channel_update(before, after):
    for x in loadedPlugins:
      client.loop.create_task(x.on_channel_update(before, after))
@client.event
async def on_channel_delete(channel):
    for x in loadedPlugins:
      client.loop.create_task(x.on_channel_delete(channel))
@client.event
async def on_member_join(member):
    for x in loadedPlugins:
      client.loop.create_task(x.on_member_join(member))
@client.event
async def on_member_remove(member):
    for x in loadedPlugins:
      client.loop.create_task(x.on_member_remove(member))
@client.event
async def on_member_update(before, after):
    for x in loadedPlugins:
      client.loop.create_task(x.on_member_update(before, after))
@client.event
async def on_server_join(server):
    for x in loadedPlugins:
      client.loop.create_task(x.on_server_join(server))
@client.event
async def on_server_update(before, after):
    for x in loadedPlugins:
      client.loop.create_task(x.on_server_update(before, after))
@client.event
async def on_server_role_create(server, role):
    for x in loadedPlugins:
      client.loop.create_task(x.on_server_role_create(server, role))
@client.event
async def on_server_role_delete(server, role):
    for x in loadedPlugins:
      client.loop.create_task(x.on_server_role_delete(server, role))
@client.event
async def on_server_role_update(server, role):
    for x in loadedPlugins:
      client.loop.create_task(x.on_server_role_update(server, role))
@client.event
async def on_member_ban(member):
    for x in loadedPlugins:
      client.loop.create_task(x.on_member_ban(member))
@client.event
async def on_member_unban(member):
    for x in loadedPlugins:
      client.loop.create_task(x.on_member_unban(member))

client.run(CONFIG.TOKEN)
