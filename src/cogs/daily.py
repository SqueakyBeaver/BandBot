from discord.ext import commands, tasks
from datetime import datetime
from database import DBClient
from cogs.holidays import Holidays
from cogs.quotes import QuotesCommands as Quotes
import dateparser
import discord
import pytz


class Daily(commands.Cog, name="daily"):
    def __init__(self, bot: commands.Bot):
        bot.bg_task = self.daily_message.start()
        self.bot: commands.Bot = bot
        self.info: DBClient = DBClient("daily")
        self.guilds: dict = self.info.find("guilds")
        self.tz = pytz.timezone("America/Chicago")
        print(self.guilds)

    @commands.command(name="test_daily")
    async def _test_daily(self, ctx: commands.Context):
        for (key, value) in self.guilds.items():
            ping_role: discord.Role = self.bot.get_guild(
                int(key)).get_role(value["role"])
        await ctx.reply(content=self.daily_quotes(ping_role), embed=self.daily_holidays())

    @tasks.loop(minutes=1)
    async def daily_message(self):
        print("checking...")
        for (key, value) in self.guilds.items():
            guild_tz = pytz.timezone(value["tz"])
            announcement_channel: discord.TextChannel = self.bot.get_channel(
                value["channel"])
            tmp_guild: discord.Guild = self.bot.get_guild(
                int(key))
            ping_role: discord.Role = tmp_guild.get_role(value["role"])
            last_sent: datetime = dateparser.parse(value["time"])

            # If it has been sent, uncheck the thing
            if value["sent"] == True and last_sent >= dateparser.parse("Today at 0:00"):
                value["sent"] = False
                print("Not sent at {0}".format(datetime.now(pytz.timezone("America/Chicago"))))

            # If it hasn't been sent and the time is after 00:00, then send it
            elif datetime.now(guild_tz) == 0 and value["sent"] == False:
                tmp_msg: discord.Message = await announcement_channel.send(self.daily_holidays())
                await tmp_msg.publish()
                await announcement_channel.send(self.daily_quotes(ping_role))
                value["sent"] = True
                value["time"] = str(datetime.now(self.tz))
                print("Sent at {0}".format(datetime.now(self.tz)))



    def daily_holidays(self):
        holidays: Holidays = Holidays(self.bot)
        return holidays.get_holidays(dateparser.parse("today"))

    def daily_quotes(self, ping_role: discord.Role):
        quotes: Quotes = Quotes(self.bot)
        quote: str = quotes.get_quotes()

        return ("{0}\n```\n{1}```".format(ping_role.mention, quote))


def setup(bot: commands.Bot):
    bot.add_cog(Daily(bot))
