from discord.ext import commands, tasks
from database import DBClient
from datetime import datetime

import asyncio
import discord


reminderDB = DBClient("dailyReminder")


class DailyReminderCommands(commands.Cog, name='Daily Reminder Commands'):

    def __init__(self, bot):
        bot.bg_task = self.daily_ping.start()
        
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


    @tasks.loop(minutes=1)
    async def daily_ping(self):
        await self.bot.wait_until_ready()

        pinged = False
        ping_channel = self.bot.get_channel(767858104066637834)

        if datetime.now().hour == 8 and not pinged:
            pinged = True
            pingUsers = reminderDB.dataset.find({})
            pingStr = ""

            for userID in pingUsers:
                user = ping_channel.guild.get_member(userID["_id"])
                pingStr += "{0} ".format(user.mention)

            await ping_channel.send("{0}\nYou are amazing, have a great day!".format(pingStr))

        if datetime.now().hour != 8:
            pinged = False


def setup(bot):
    bot.add_cog(DailyReminderCommands(bot))
