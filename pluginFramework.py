import inspect
from attributes import userCommand
from attributes import backgroundLoop
from attributes import afterCheck
import CONFIG
import discord


class pluginShell(object):


    def __init__(self, clientInstance):
        self.clientInstance = clientInstance
        self.userCommands = {}
        self.backgroundLoops = []
        self.afterChecks = []
        #fetch all methods
        for name, member in inspect.getmembers(self):
            if hasattr(member, "isCommand"):
                self.userCommands[member.__name__] = member
            if hasattr(member, "isLoop"):
                self.backgroundLoops.append(member)
                #create loops for all background processses
                self.clientInstance.loop.create_task(member())
            if hasattr(member, "afterCheck"):
                self.afterChecks.append(member)




    async def _on_message(self, message):
        if message.author != self.clientInstance.user:
            command = message.content.split()
            commandStr = command[0]
            if commandStr.startswith(CONFIG.PREFIX):
                commandStr = commandStr.replace(CONFIG.PREFIX, "")
                if commandStr in self.userCommands.keys():
                    await self.userCommands[commandStr](message)

            for x in self.afterChecks:
                try:
                    await x(message)
                except:
                    pass

    async def on_message(self, message):
        pass

    async def on_message_edit(self, before, after):
        pass

    async def on_message_delete(self, message):
        pass

    async def on_channel_create(self, channel):
        pass

    async def on_channel_update(self, before, after):
        pass

    async def on_channel_delete(self, channel):
        pass

    async def on_member_join(self, member):
        pass

    async def on_member_remove(self, member):
        pass

    async def on_member_update(self, before, after):
        pass

    async def on_server_join(self, server):
        pass

    async def on_server_update(self, before, after):
        pass

    async def on_server_role_create(self, server, role):
        pass

    async def on_server_role_delete(self, server, role):
        pass

    async def on_server_role_update(self, server, role):
        pass

    async def on_member_ban(self, member):
        pass

    async def on_member_unban(self, member):
        pass
