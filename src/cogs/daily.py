from discord.ext import commands, tasks
from datetime import datetime
from database import DBClient
from cogs.holidays import Holidays
from cogs.quotes import QuotesCommands as Quotes
import dateparser
import discord
import logging
import pytz


class Daily(commands.Cog, name="daily"):
    def __init__(self, bot: commands.Bot):
        self.daily_message.start()
        self.bot = bot
        self.info: DBClient = DBClient("daily")
        self.guilds: dict = self.info.find("guilds")
        self.tz = pytz.timezone("America/Chicago")

    @commands.command(name="test_daily")
    async def _test_daily(self, ctx: commands.Context):
        for (key, value) in self.guilds.items():
            ping_role: discord.Role = self.bot.get_guild(int(key)).get_role(
                value["role"])
        await ctx.reply(content=self.daily_quotes(ping_role),
                        embed=self.daily_holidays())

    def update(self):
        logging.info("Updating\n___________")
        self.info: DBClient = DBClient("daily")
        self.guilds: dict = self.info.find("guilds")
        logging.info(self.guilds)

    @tasks.loop(minutes=1)
    async def daily_message(self):
        await self.bot.wait_until_ready()
        self.update()
        logging.info("checking...")
        for (key, value) in self.guilds.items():
            logging.info(key)
            if self.bot.get_guild(int(key)):
                logging.info(self.bot.get_guild(int(key)).name)

            guild_tz = pytz.timezone(value["tz"]) if value["tz"] else None
            last_sent: datetime = dateparser.parse(value["time"])

            tmp_guild = self.bot.get_guild(int(key))
            ping_role = tmp_guild.get_role(value["role"])
            logging.info("Last Sent for {0}: {1}".format(
                tmp_guild.name, str(last_sent)))

            # If it has been sent, uncheck the thing
            if last_sent >= dateparser.parse("Today at 0:00" + value["time"][-6:]):
                logging.info("Not sent at {0}".format(
                    datetime.now(pytz.timezone("America/Chicago"))))

            # If it is the time to send it and it hasn't been sent today, send it
            elif last_sent < dateparser.parse(
                    "Today at 0:00" + value["time"][-6:]):
                if announcement_channel := self.bot.get_channel(
                        value["channel"]):
                    tmp_msg = await announcement_channel.send(
                        embed=self.daily_holidays())
                    await tmp_msg.publish()
                    await announcement_channel.send(
                        self.daily_quotes(ping_role))
                    value["sent"] = True
                    value["time"] = str(datetime.now(guild_tz))
                    logging.info("Sent at {0}".format(
                        datetime.now(self.tz)))
                self.info.update("guilds", self.guilds)

    def daily_holidays(self):
        holidays: Holidays = Holidays(self.bot)
        return holidays.get_holidays(dateparser.parse("today"))

    def daily_quotes(self, ping_role: discord.Role):
        quotes: Quotes = Quotes(self.bot)
        quote: str = quotes.get_quotes()

        return ("{0}\n```\n{1}```".format(ping_role.mention, quote))


def setup(bot: commands.Bot):
    bot.add_cog(Daily(bot))
