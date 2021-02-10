from main import BotClient
from discord.ext import commands, tasks
from database import DBClient
from datetime import datetime

import asyncio
import discord


reminderDB = DBClient("dailyReminder")


class DailyReminderCommands(commands.Cog, name='Daily Reminder Commands'):

    def __init__(self, bot: BotClient):
        bot.bg_task = bot.loop.create_task(self.daily_ping())
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


def setup(bot):
    bot.add_cog(DailyReminderCommands(bot))
