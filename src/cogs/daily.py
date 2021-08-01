from discord.ext import commands, tasks
from datetime import datetime
from database import DBClient
from cogs.holidays import Holidays
from cogs.quotes import Quotes
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
        time = datetime.now()
        ping_role: discord.Role = self.bot.get_guild(ctx.guild.id).get_role(
            self.guilds[str(ctx.guild.id)]["role"])
        await ctx.reply(content=self.daily_quotes(ping_role) + str(datetime.now() - time),
                        embed=self.daily_holidays())

    def update(self):
        logging.info("\n\nUpdating")
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
            sent = value["sent"]

            tmp_guild = self.bot.get_guild(int(key))
            ping_role = tmp_guild.get_role(value["role"])
            logging.info("Sent for {0} already: {1}".format(
                tmp_guild.name, value["sent"]))

            if datetime.now(guild_tz).hour == 0 and not sent:
                value["sent"] = True
                logging.info("Sent")

                if announcement_channel := self.bot.get_channel(
                        value["channel"]):
                    tmp_msg = await announcement_channel.send(
                        embed=self.daily_holidays(guild_tz))
                    await tmp_msg.publish()
                    await tmp_msg.start_thread("Holiday Discussion")
                    tmp_msg = await announcement_channel.send(
                        self.daily_quotes(ping_role))
                    await tmp_msg.start_thread("QOTD Discussion")


            elif datetime.now(guild_tz).hour > 0:
                logging.info("not sent")
                value["sent"] = False

            self.guilds[key] = value
            self.info.update("guilds", self.guilds)

            logging.info("\n")

    def daily_holidays(self, tz):
        return Holidays.get_holidays(datetime.now(tz))

    def daily_quotes(self, ping_role: discord.Role):
        quote: str = Quotes.get_quotes()

        return ("{0}\n```\n{1}```".format(ping_role.mention, quote))


def setup(bot: commands.Bot):
    bot.add_cog(Daily(bot))
