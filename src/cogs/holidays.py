from database import DBClient
from datetime import datetime
from discord.ext import commands, tasks
from bs4 import BeautifulSoup

import requests
import discord
import pytz
import dateparser


class Holidays(commands.Cog, name="holiday"):
    """ Commands to find holidays from checkiday.com """

    def __init__(self, bot):
        bot.daily_holidays_loop = self.daily_holidays.start()
        self.bot = bot
        self.holiday_info: DBClient = DBClient("daily")
        self.guilds = self.holiday_info.find("guilds")

    def get_holidays(self, date):
        link = f"https://www.checkiday.com/{date.month}/{date.day}/{date.year}"

        try:
            site = requests.get(link)
        except Exception as e:
            return

        soup = BeautifulSoup(site.content, "html.parser")

        holidays = soup.find(id="masonryGrid")
        links = holidays.find_all("a")

        links_list: list[str] = []
        for i in links:
            if i.string is None:
                links_list.append(i.get('href'))

        links_list = list(set(links_list))
        desc_str = ""
        for i in links_list:
            sep = i.split('/')

            if "timeanddate.com" in i:
                if len(desc_str + f"\n**- On This Day in History**\n[Learn More]({i})\n") < 2048:
                    desc_str += f"\n**- On This Day in History**\n[Learn More]({i})\n"
                continue
            if len(desc_str + f"\n**- {sep[-1].replace('-', ' ').title()}**\n[Learn More]({i})\n") < 2048:
                desc_str += f"\n**- {sep[-1].replace('-', ' ').title()}**\n[Learn More]({i})\n"

        res = discord.Embed(title=f"Holidays for {'0' if date.month < 10 else ''}"
                            f"{date.month}/{'0' if date.day < 10 else ''}{date.day}/{date.year}",
                            description=desc_str, url=link)

        res.set_footer(text=f"{len(links_list)} results",
                       icon_url="https://i.pinimg.com/originals/b0/b8/5c/b0b85cd8797638d0c80035f572b0cbd3.jpg")  # I know it's a a jpg, I'm sorry

        return res

    @commands.command(
        name="holidays",
        description="Get holidays for a specific date.",
        aliases=["h"]
    )
    async def _holidays(self, ctx: commands.Context, *, day: str):
        date = dateparser.parse(day)

        res = self.get_holidays(date)

        if res is None:
            return await ctx.reply(f"{ctx.author.mention} No results found :(")

        await ctx.reply(ctx.author.mention, embed=res)

    @tasks.loop(minutes=1)
    async def daily_holidays(self):
        await self.bot.wait_until_ready()

        for i in self.guilds.values():
            try:
                tz = pytz.timezone(i["tz"])

                if datetime.now(tz).hour == 0 and not i["sent"]:  # Please work
                    i["sent"] = True

                    send_to: discord.TextChannel = self.bot.get_channel(
                        i["channel"])

                    res = self.get_holidays(dateparser.parse("today"))
                    sent: discord.Message = await send_to.send(embed=res)
                    await sent.publish()

                if datetime.now(tz).hour != 0:
                    i["sent"] = False
            except:
                continue


    @commands.group(name="holiday")
    async def _holiday_group(self, ctx: commands.Context, *, args):
        if ctx.invoked_subcommand == None:
            await self._holidays(ctx, args)



def setup(bot):
    bot.add_cog(Holidays(bot))
