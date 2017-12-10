from pluginFramework import pluginShell
from attributes import userCommand
from attributes import backgroundLoop
import asyncio
import discord
import random

import CONFIG

class Raffle(pluginShell):


#TODO CLEAN UP CODE


    @userCommand
    async def raffle(self, message):
        approvedRoles = set()
        for x in CONFIG.RAFFLE_APPROVED_IDS:
            approvedRoles.add(discord.utils.get(
                message.server.roles, id = x))
        authorRoles = set()
        for x in message.author.roles:
            authorRoles.add(x)
        #misc variables
        printStr = ""
        #only run if in those roles
        if (len(approvedRoles & authorRoles) != 0):
            #int check used for prompts
            def intCheck(msg):
                return msg.content.isdigit()
            #prompt for time
            await self.clientInstance.send_message(message.channel,
                'Open raffle for how many seconds?')
            waitMsg = await self.clientInstance.wait_for_message(timeout=100.0,
                author = message.author, check = intCheck)
            wait = int(waitMsg.content)
            #prompt for winners
            await self.clientInstance.send_message(message.channel,
                'How many winners should be drawn?')
            rollsMsg = await self.clientInstance.wait_for_message(timeout=100.0,
                author = message.author, check = intCheck)
            rolls = int(rollsMsg.content)
            #prompt for additional info
            await self.clientInstance.send_message(message.channel,
                'Any additional info? Include pictures as links.')
            additional = await self.clientInstance.wait_for_message(timeout=100.0,
                author = message.author, check = None)
            #Sends Message to clarity entry requirements
            botMsg = await self.clientInstance.send_message(message.channel,
                """The raffle of {} winners will end after {} seconds.
                React to this message with 😮 to enter.
                Additional Info: {}""".format(rolls, wait, additional.content))
            #pins bot message
            await self.clientInstance.pin_message(botMsg)
            #Adds Reaction to use for entry
            await self.clientInstance.add_reaction(botMsg,"😮")
            #wait desired period
            await asyncio.sleep(wait)
            #some bug with getting message reactions.
            #This refetches the message.
            botMsg2 = await self.clientInstance.get_message(message.channel, botMsg.id)
            #From message, grabs the reaction object
            for react in botMsg2.reactions:
                if str(react.emoji) == "😮":
                    reaction = react
            #fetches list of users that added reaction
            users = await self.clientInstance.get_reaction_users(reaction)
            #remove bot from entries
            users.remove(self.clientInstance.user)
            #adds users to list
            for user in users:
                printStr += user.mention + " "
            #mentions all entered users
            await self.clientInstance.send_message(message.channel, str(len(users))
                +" member(s) have entered: " + printStr)
            await asyncio.sleep(5)
            #choses random user
            for x in range(0,int(rolls)):
                winner = random.choice(users)
                await self.clientInstance.send_message(message.channel,
                    "Winner {} of {} is ".format(x+1, rolls)
                    + winner.mention)
            await self.clientInstance.unpin_message(botMsg)
        #people apprently dont understand the bot so...a pm reminder
        else:
            await self.clientInstance.send_message(message.author,
                """
                The raffle command can only be run by Artisans, GB, Vendors.
                If you are trying to enter a raffle. See the channel pins for directions on how to enter.
                `!raffle` does not enter you into the raffle.
                Please follow the directions listed in the pinned bot message.
                """)
