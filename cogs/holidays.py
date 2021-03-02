import requests
from bs4 import BeautifulSoup
from discord.ext import commands, tasks
import discord
import pytz
import dateparser
from datetime import datetime


class Holidays(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_holidays(self, date):
        link = f"https://www.checkiday.com/{date.month}/{date.day}/{date.year}"
        res = []

        try:
            site = requests.get(link)
        except Exception as e:
            return res.append(f"ERROR: {e}")

        soup = BeautifulSoup(site.content, "html.parser")

        holidays = soup.find(id="masonryGrid")
        links = holidays.find_all("a")

        links_list: list[str] = []
        for i in links:
            if i.string is None:
                links_list.append(i.get('href'))

        links_list = list(set(links_list))
        for i in links_list:
            sep = i.split('/')

            if "timeanddate.com" in i:
                res.append(f"[`On This Day in History`]({i})")
                continue
            res.append(f"[`{sep[-1].replace('-', ' ').title()}`]({i})")

        return res

    @commands.command(
        name="holidays",
        description="Get holidays for a specific date.",
        aliases=["h"]
    )
    async def _holidays(self, ctx, *, day):
        date = dateparser.parse(day)

        res = self.get_holidays(date)
        if "ERROR" in res[0]:  # Thank you Title case for making this possible
            return await ctx.send(f"{ctx.author.mention}\n{res[0]}")

        if res[0] is None:
            return await ctx.send(f"{ctx.author.mention} No results found :(")

        count = sum(1 for i in res)

        res_str = ""
        for i in res:
            res_str += i + "\n"
            print(i)

        e = discord.Embed(title=f"Holidays for {'0' if date.month < 10 else ''}"
                          f"{date.month}/{'0' if date.day < 10 else ''}{date.day}/{date.year}", description=res_str,)

        e.set_footer(text=f"{count} results",
                     icon_url="https://i.pinimg.com/originals/b0/b8/5c/b0b85cd8797638d0c80035f572b0cbd3.jpg")  # I know it's a a jpg, I'm sorry

        await ctx.send(ctx.author.mention, embed=e)

    @tasks.loop(minutes=1)
    async def daily_holidays(self):
        await self.bot.wait_until_ready()

        white_board = self.bot.get_channel(767843340137529397)
        tz = pytz.timezone("America/Chicago")

        if datetime.now(tz).hour == 0:  # Please work
            res = self.get_holidays("today")
            if "ERROR" in res[0]:  # Thank you Title case for making this possible
                return await white_board.send(f"{white_board.author.mention}\n{res.__next__()}")

            if res[0] is None:
                return await white_board.send(f"{white_board.author.mention} No results found :(")

            count = sum(1 for i in res)

            res_str = ""
            for i in res:
                res_str += i + "\n"
                print(i)

            e = discord.Embed(title=f"Today's Holidays", description=res_str,)
            # AAAAAAAAAAA IT'S A JPEG?!!
            e.set_footer(text=f"There are {count} holidays today",
                         icon_url="https://i.pinimg.com/originals/b0/b8/5c/b0b85cd8797638d0c80035f572b0cbd3.jpg")

            await white_board.send(embed=e)


def setup(bot):
    bot.add_cog(Holidays(bot))
