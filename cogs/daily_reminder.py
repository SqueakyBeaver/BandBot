from discord.ext import commands
from database import DBClient
from datetime import datetime, timedelta, timezone
import pytz


reminderDB = DBClient("dailyReminder", name="Daily Reminder Commands")

class DailyReminderCommands(commands.Cog):

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


async def daily_ping(botClient):
    await botClient.wait_until_ready()
    ping_channel = botClient.get_channel(767858104066637834)
    pinged = False
    while not botClient.is_closed():
        localTimezone = pytz.timezone('America/Chicago')
        if (datetime.now(localTimezone).hour == 3):
            pingUsers = reminderDB.dataset.find({})
            if (not pinged):
                pingStr = ""
                for userID in pingUsers:
                    user = ping_channel.guild.get_member(userID["_id"])
                    pingStr += f"{user.mention} "
                await ping_channel.send(f"{pingStr}\nYou are amazing, have a great day!")
                pinged = True
        else:
            pinged = False
            return


def setup(bot):
    bot.add_cog(DailyReminderCommands(bot))
