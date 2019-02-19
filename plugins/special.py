from pluginFramework import pluginShell
from attributes import userCommand
from attributes import backgroundLoop
import asyncio
import discord
import textwrap
import re

import CONFIG

class Sony(pluginShell):

    #TODO add exception handeling
    @userCommand
    async def executecode(self, message):
        if message.author.id == "1FIXME_USERID":
            env = {
                'client': self.clientInstance,
                'channel': message.channel,
                'author': message.author,
                'server': message.server,
                'message': message,
            }


            env.update(globals())
            commandStr = message.content.split("```")[-2]
            toExec = 'async def func():\n%s' % textwrap.indent(commandStr, '  ')
            print(toExec)
            exec(toExec, env)
            func = env['func']
            await func()
