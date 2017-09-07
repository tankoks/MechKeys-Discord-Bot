# -*- coding: utf-8 -*-
import discord
import asyncio
import time
import random
import datetime
import pickle
import re

client = discord.Client()
@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#Global Variables
#Region Role IDs
roleIDs = ["317376455627636736", "317376733340762114", "317376486640189440",
    "317376594127749120", "317376721655562240", "317376869638864927",
    "317376875183996929", "317389130671718400"]
Rdy = False


#Statistics Record Variables
#Load from pickle if it exist
#Else create new instances
try:
    writeToPickle = pickle.load(open( "save.p", "rb"))
    toDay = writeToPickle[0]
    messageCount = writeToPickle[1]
    newMembers = writeToPickle[2]
    leftMembers = writeToPickle[3]
    activeMembersWeek = writeToPickle[4]
    print("pickle loaded")
except:
    toDay = datetime.datetime.today()
    messageCount = [0,0,0,0,0,0,0,0]
    newMembers = 0
    leftMembers = 0
    activeMembersWeek = [{},{},{},{},{},{},{},{},{}]
    print("pickle file doesnt exist. new instances created")





#Commands
@client.event
async def on_message(message):
    global Rdy
    birb = discord.utils.get(message.server.roles,
        id = "339142115126935554")

    #Statistics Keeping Information.
    messageCount[0] += 1
    messageCount[7] += 1
    activeMembersWeek[0][message.author] = 1
    activeMembersWeek[7][message.author] = 1

    #Vote command. Adds thumbsup and thumbs down emojis to message
    #containing !vote
    if message.content.lower().startswith("!vote"):
        await client.add_reaction(message,"👍")
        await client.add_reaction(message,"👎")


    #Region Roles


    #Adds Australia Region Role. Calls AddRegionRole helper.
    if message.content.lower().startswith("!aus"):
        await addRegionRole(message, message.author, "317376875183996929")
    #Adds Europe Region Role. Calls AddRegionRole helper.
    if message.content.lower().startswith("!eu"):
        await addRegionRole(message, message.author, "317376455627636736")
    #Adds South East Asia Region Role. Calls AddRegionRole helper.
    if message.content.lower().startswith("!sea"):
        await addRegionRole(message, message.author, "317376733340762114")
    #Adds South America Region Role. Calls AddRegionRole helper.
    if message.content.lower().startswith("!sa"):
        await addRegionRole(message, message.author, "317376594127749120")
    #Adds North America Region Role. Calls AddRegionRole helper.
    if message.content.lower().startswith("!na"):
        await addRegionRole(message, message.author, "317376486640189440")
    #Adds Africa Region Role. Calls AddRegionRole helper.
    if message.content.lower().startswith("!africa"):
        await addRegionRole(message, message.author, "317376721655562240")
    #Adds Asia Region Role. Calls AddRegionRole helper.
    if message.content.lower().startswith("!asia"):
        await addRegionRole(message, message.author, "317376869638864927")
    #Adds Middle East Region Role. Calls AddRegionRole helper.
    if message.content.lower().startswith("!me"):
        await addRegionRole(message, message.author, "317389130671718400")

    #Admin Functions
    #Purge messages from given channel
    if message.content.lower().startswith("!purge"):
        mods = discord.utils.get(
            message.server.roles, id = "190330163743948800")
        if mods in message.author.roles:
            num = re.sub(r'\D', '', message.content)
            if num != "":
                await client.purge_from(message.channel,
                    limit = int(num))
            else:
                def intCheck(msg):
                    return msg.content.isdigit()

                await client.send_message(message.channel,
                    'Purge how many messages?')
                purgeNum = await client.wait_for_message(timeout=100.0,
                    author = message.author, check = intCheck)
                await client.purge_from(message.channel,
                    limit = int(purgeNum.content))


    #Statistics
    #Admin Print Stats
    if message.content.lower().startswith("!stats"):
        mods = discord.utils.get(
            message.server.roles, id = "190330163743948800")
        if mods in message.author.roles:
            weekActive = [0,0,0,0,0,0,0]
            for x in range(0,7):
                weekActive[x] = len(activeMembersWeek[x])
            await client.send_message(message.channel,
                "Stats as of {}\n".format(datetime.datetime.now())
                    + "Last Reset: {}\n".format(toDay)
                    + "Messages Today: {}\n".format(messageCount[0])
                    + "Messages Last 7 Days: {}\n".format(messageCount[0:7])
                    + "Messages 7 Day Total: {}\n".format(messageCount[7])
                    + "Active Members Today: {}\n"
                        .format(len(activeMembersWeek[0]))
                    + "Average Messages Per Active Member Today: {}\n"
                        .format(messageCount[0]/len(activeMembersWeek[0]))
                    + "Active This Week: {}\n".format(weekActive)
                    + "Unique Active This Week Total: {}\n"
                        .format(len(activeMembersWeek[7]))
                    + "Number of New Member Today: {}\n".format(newMembers)
                    + "Number of Left Member Today: {}\n".format(leftMembers)
                    + "Net Gain 24h: {}\n".format(newMembers - leftMembers)
                    + "Total Members: {}".format(message.server.member_count) )


    #raffle function
    if message.content.lower().startswith("!raffle"):
        #roll permissions
        vendor = discord.utils.get(
            message.server.roles, id = "190336426427023360")
        gb = discord.utils.get(
            message.server.roles, id = "306371523579740164")
        artisan = discord.utils.get(
            message.server.roles, id = "284779538783666196")
        #misc variables
        printStr = ""
        #only run if in those roles
        if (vendor in message.author.roles
            or gb in message.author.roles
            or artisan in message.author.roles):
            #int check used for prompts
            def intCheck(msg):
                return msg.content.isdigit()
            #prompt for time
            await client.send_message(message.channel,
                'Open raffle for how many seconds?')
            waitMsg = await client.wait_for_message(timeout=100.0,
                author = message.author, check = intCheck)
            wait = int(waitMsg.content)
            #prompt for winners
            await client.send_message(message.channel,
                'How many winners should be drawn?')
            rollsMsg = await client.wait_for_message(timeout=100.0,
                author = message.author, check = intCheck)
            rolls = int(rollsMsg.content)
            #prompt for additional info
            await client.send_message(message.channel,
                'Any additional info? Include pictures as links.')
            additional = await client.wait_for_message(timeout=100.0,
                author = message.author, check = None)
            #Sends Message to clarity entry requirements
            botMsg = await client.send_message(message.channel,
                "The raffle of {} winners will end after {} seconds."
                    .format(rolls, wait)
                + "\nReact to this message with 😮 to enter."
                + "\nAdditional Info: " + additional.content)
            #pins bot message
            await client.pin_message(botMsg)
            #Adds Reaction to use for entry
            await client.add_reaction(botMsg,"😮")
            #wait desired period
            await asyncio.sleep(wait)
            #some bug with getting message reactions.
            #This refetches the message.
            botMsg2 = await client.get_message(message.channel, botMsg.id)
            #From message, grabs the reaction object
            for react in botMsg2.reactions:
                if str(react.emoji) == "😮":
                    reaction = react
            #fetches list of users that added reaction
            users = await client.get_reaction_users(reaction)
            #remove bot from entries
            users.remove(client.user)
            #adds users to list
            for user in users:
                printStr += user.mention + " "
            #mentions all entered users
            await client.send_message(message.channel, str(len(users))
                +" member(s) have entered: " + printStr)
            await asyncio.sleep(5)
            #choses random user
            for x in range(0,int(rolls)):
                winner = random.choice(users)
                await client.send_message(message.channel,
                    "Winner {} of {} is ".format(x+1, rolls)
                    + winner.mention)
            await client.unpin_message(botMsg)
        #people apprently dont understand the bot so...a pm reminder
        else:
            await client.send_message(message.author,
                "The raffle command can only be run by Artisans, GB, Vendors.\n"
                + "If you are trying to enter a raffle. See the channel pins "
                + "for directions on how to enter.\n"
                + "`!raffle` does not enter you into the raffle. Please "
                + "follow the directions listed in the pinned bot message.")

    #Temp Roles

    #Adds Birb role for artisan flash sale chat access.
    #Calls addTempRole
    if ("I understand that this channel"
        + " will have everyone pings"
        + " and that abusing them can result in a ban."
        + " I also understand that this channel is a privilege."
        + " I am entitled to everything."
        + " Sony is a piece of ####."
        + " I deserve everything." in message.content
        or message.content.lower().startswith("!flashsale")):
        await addTempRole(message, message.author, "339142115126935554")

    if message.mention_everyone or birb in message.role_mentions:
        #test 338895331234152451
        #verified 256281441078345752
        #birb 334376153265733634
        #sugbox 331887065564315648
        #kbartisans 278960636153692160
        if Rrd:
            await etftroll(False, message)
            print ("hidden")
            await asyncio.sleep(1200)
            await etftroll(None, message)
            print ("not hidden")


    if message.content.lower().startswith("!birdsalt"):
        if message.author.id == "142750185380904960":
            if Rdy:
                Rdy = False
            else:
                Rdy = True
            await client.send_message(message.author,
                "Salt = {}".format(Rdy))



#Helpers
#Troll with ETF
async def etftroll(perm, message):
    birb = discord.utils.get(message.server.roles,
        id = "339142115126935554")
    verified = discord.utils.get(message.server.roles,
        id = "256281441078345752")
    kbartisans = discord.utils.get(message.server.channels,
        id = "278960636153692160")
    birbwatch = discord.utils.get(message.server.channels,
        id = "334378179206840335")
    for chans in message.server.channels:
        try:
            overwrite = discord.PermissionOverwrite()
            overwrite.send_messages = perm
            overwrite.connect = perm
            await client.edit_channel_permissions(chans, birb, overwrite)
        except:
            pass

    if perm == None:
        perm = True
    for chan in [kbartisans]:
        try:
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = perm
            overwrite.send_messages = perm
            overwrite.connect = perm
            await client.edit_channel_permissions(
                chan, verified, overwrite)
        except:
            pass
    for chan in [birbwatch]:
        try:
            overwrite = discord.PermissionOverwrite()
            overwrite.read_messages = perm
            overwrite.send_messages = perm
            overwrite.mention_everyone = perm
            overwrite.connect = perm
            await client.edit_channel_permissions(
                chan, birb, overwrite)
        except:
            pass
#Helper Function to add Region Roles.
async def addRegionRole(message, member, role):
    rolelist = []
    for memberroles in member.roles:
        rolelist.append(memberroles.id)
        for IDs in roleIDs:
            if IDs in rolelist:
                await client.send_message(message.channel,
                    "You already have a region. Contact a Mod.")
                return
            else:
                continue
    roleAdd = discord.utils.get(message.server.roles,
        id = role)
    await client.add_roles(member, roleAdd)
    await client.delete_message(message)

#Helper Function to add Temp Roles.
async def addTempRole(message, member, role):
    for memberroles in message.author.roles:
        if memberroles.id == role:
            roleAdd = discord.utils.get(message.server.roles,
                id = role)
            await client.remove_roles(message.author, roleAdd)
            await client.delete_message(message)
            return
        else:
            continue
    roleAdd = discord.utils.get(message.server.roles,
        id = role)
    await client.add_roles(message.author, roleAdd)
    await client.delete_message(message)

#Counts number of members that leave the server for statistics.
@client.event
async def on_member_remove(member):
    global leftMembers
    leftMembers += 1

#Counts number of members that join the server for statistics.
@client.event
async def on_member_join(member):
    global newMembers
    newMembers += 1

#Background Tasks
async def my_background_task():
    #Update Stats
    global toDay
    global activeMembersWeek
    global newMembers
    global leftMembers
    global messageCount
    global writeToPickle
    await client.wait_until_ready()
    #If next Day
    while not client.is_closed:
        writeToPickle = [toDay, messageCount, newMembers,
            leftMembers, activeMembersWeek]
        pickle.dump(writeToPickle, open("save.p", "wb"))
        if datetime.datetime.now().day != toDay.day:
            #fetch server
            server = client.get_server("190327149696253952")
            #print to file
            dataFile = open("data.csv" , "w")
            dataFile.write(
            "{},{},{},{},{},{},{},{}\n".format(
                toDay,
                datetime.datetime.now(),
                server.member_count,
                newMembers,
                leftMembers,
                len(activeMembersWeek[0]),
                len(activeMembersWeek[7]),
                messageCount[0]))
            dataFile.close()
            #Reset Stat Numbers
            newMembers = 0
            leftMembers = 0
            #recalculate 7 day stats
            activeMembersWeek[7] = {}
            for days in range(6,0,-1):
                messageCount[days] = messageCount[days - 1]
                activeMembersWeek[days] = activeMembersWeek[days - 1]
                activeMembersWeek[7].update(activeMembersWeek[days])
            messageCount[0] = 0
            activeMembersWeek[0] = {}
            messageCount[7] = sum(messageCount[0:6])
            toDay = datetime.datetime.today()
            print("saving @ {}".format(toDay))
        await asyncio.sleep(60)

client.loop.create_task(my_background_task())
#bot token
client.run('###')
