from discord.ext import commands
from database import DBClient

class DailyReminderCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reminderDB = DBClient("dailyReminder")

    @commands.command(name='joinping',
                      aliases=['joinreminder'],
                      description="Join the daily ping reminder")
    async def join_reminder(self, ctx):
        if (self.reminderDB.find(ctx.message.author.id) is None):
            self.reminderDB.add_ping(ctx.message.author.id)
            await ctx.send("Successfully joined the daily reminder")
        else:
            await ctx.send("You're already in the daily reminder..")

    @commands.command(name='leaveping',
                      aliases=['lp', 'leavereminder'],
                      description="Leave the daily reminder because you don't like pings")
    async def leave_ping(self, ctx):
        if (self.reminderDB.find(ctx.message.author.id) is not None):
            self.reminderDB.delete({"_id": ctx.message.author.id})
            await ctx.send("Hope you like your ping-free like")
        else:
            await ctx.send("You can't leave something you never joined")


def setup(bot):
    bot.add_cog(DailyReminderCommands(bot))
