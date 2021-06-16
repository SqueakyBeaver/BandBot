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
        self.bot = bot

    @staticmethod
    def get_holidays(date):
        link = f"https://www.checkiday.com/{date.month}/{date.day}/{date.year}"

        try:
            site = requests.get(link)
        except Exception:
            return

        soup = BeautifulSoup(site.content, "html.parser")

        links = soup.find(id="magicGrid").find_all("a")

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

        res = Holidays.get_holidays(date)

        if res is None:
            return await ctx.reply(f"{ctx.author.mention} No results found :(")

        await ctx.reply(ctx.author.mention, embed=res)



    @commands.group(name="holiday")
    async def _holiday_group(self, ctx: commands.Context, *, args):
        if ctx.invoked_subcommand == None:
            await self._holidays(ctx, args)



def setup(bot):
    bot.add_cog(Holidays(bot))
