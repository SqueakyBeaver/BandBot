from discord.ext import commands
from database import DBClient
from datetime import datetime

import asyncio
import discord


reminderDB = DBClient("dailyReminder")


class DailyReminderCommands(commands.Cog, name='Daily Reminder Commands'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='joinping',
                      aliases=['joinreminder', 'jr', 'jp'],
                      description="Join the daily ping reminder")
    async def join_reminder(self, ctx):
        if (reminderDB.find(ctx.message.author.id) is None):
            reminderDB.add_ping(ctx.message.author.id)
            await ctx.send("Successfully joined the daily reminder")
        else:
            await ctx.send("You're already in the daily reminder..")

    @commands.command(name='leaveping',
                      aliases=['lp', 'leavereminder', 'lr'],
                      description="Leave the daily reminder because you don't like pings")
    async def leave_ping(self, ctx):
        if (reminderDB.find(ctx.message.author.id) is not None):
            reminderDB.delete({"_id": ctx.message.author.id})
            await ctx.send("Hope you like your ping-free like")
        else:
            await ctx.send("You can't leave something you never joined")


async def daily_ping(botClient: discord.Client):
    await botClient.wait_until_ready()
    ping_channel = botClient.get_channel(767858104066637834)
    while not botClient.is_closed():
        if (datetime.now().hour == 8):
            pingUsers = reminderDB.dataset.find({})
            pingStr = ""
            for userID in pingUsers:
                user = ping_channel.guild.get_member(userID["_id"])
                pingStr += "{0} ".format(user.mention)
            await ping_channel.send("{0}\nYou are amazing, have a great day!".format(pingStr))
            await asyncio.sleep(3600)


def setup(bot):
    bot.add_cog(DailyReminderCommands(bot))
