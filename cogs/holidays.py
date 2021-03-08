from cgitb import reset
import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
import discord
import pytz
import dateparser
from datetime import datetime


class Holidays(commands.Cog):
    def __init__(self, bot):
        bot.daily_holidays_loop = self.daily_holidays.start()
        self.already_sent = False
        self.bot = bot

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
                desc_str += f"**On This Day in History**\n[Learn More]({i})\n"
                continue
            desc_str += f"**{sep[-1].replace('-', ' ').title()}**\n[Learn More]({i})\n"

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
    async def _holidays(self, ctx, *, day):
        date = dateparser.parse(day)

        res = self.get_holidays(date)

        if res is None:
            return await ctx.send(f"{ctx.author.mention} No results found :(")

        await ctx.send(ctx.author.mention, embed=res)

    @tasks.loop(minutes=1)
    async def daily_holidays(self):
        await self.bot.wait_until_ready()

        white_board = self.bot.get_channel(767843340137529397)
        cst = pytz.timezone("America/Chicago")

        if datetime.now(cst).hour == 0 and not self.already_sent:  # Please work
            print("In")  # Debugging
            self.already_sent = True

            res = self.get_holidays(dateparser.parse("today"))
            await white_board.send(embed=res)

        if datetime.now(cst).hour != 0:
            self.already_sent = False


def setup(bot):
    bot.add_cog(Holidays(bot))
