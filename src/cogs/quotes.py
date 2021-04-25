from discord.ext import commands, tasks
from datetime import datetime
from database import DBClient

import asyncio
import discord
import wikiquote
import random
import pytz


class QuotesCommands(commands.Cog, name="quotes"):
    """ Commands for Quotes """

    def __init__(self, bot):
        bot.bg_task = self.daily_ping.start()
        self.bot: commands.Bot = bot
        self.quote_info: DBClient = DBClient("daily")
        self.guilds: dict = self.quote_info.find("guilds")
        print(self.guilds)

    def get_quotes(self):
        daily_quote = wikiquote.quote_of_the_day()
        return f"{daily_quote[0]}\n~{daily_quote[1]}"

    @commands.command(name='joinping',
                      aliases=['jp'],
                      description="Join the daily quote ping")
    async def join_reminder(self, ctx: commands.Context):
        if (ctx.guild.get_role(830888283835203635) not in ctx.author.roles):
            return await ctx.reply("Successfully joined the quote of the day ping!")

        await ctx.reply("You're already in the quote of the day ping...")

    @commands.command(name='leaveping',
                      aliases=['lp'],
                      description="Leave the daily quote pinging because you don't like pings")
    async def leave_ping(self, ctx):
        if (ctx.guild.get_role(830888283835203635) in ctx.author.roles):
            return await ctx.reply("Hope you enjoy your ping-free life")

        await ctx.reply("You can't leave something you never joined")

    @commands.command(
        name="quote",
        description="Random quote from WikiQuote",
        usage="[search]"
    )
    async def _quote(self, ctx, *query):
        if ' '.join(query):
            res = wikiquote.quotes(random.choice(
                wikiquote.search(' '.join(query).strip())))
            if not res:
                return await ctx.reply(f'No quotes from {" ".join(query).strip()}')
            return await ctx.reply(f'```\n{res[0]}\n~{" ".join(query).strip()}```')

        def check(author):
            def inner_check(message):
                return message.author == author
            return inner_check

        try:
            await ctx.reply("Would you like a random quote? `Yes/No`\nYou have 30 seconds to respond")
            answer = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.reply("You took too long, stupid slow human")

        if "y" in answer.content.lower():
            author = random.choice(wikiquote.random_titles())
            res = random.choice(wikiquote.quotes(author))
            return await ctx.reply(f'```\n{res}\n~{author}```')
        elif not "n" in answer.content.lower():
            return await ctx.reply("Invalid choice!")

        try:
            await ctx.reply("What would you like to search for? \nYou have 30 seconds to respond")
            answer = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.reply("You took too long, stupid slow human")

        search_res = wikiquote.search(answer.content.strip())
        res = ""
        for i in search_res:
            res += f'{search_res.index(i) + 1}. {i}\n'

        def check2(author):
            def inner_check(message):
                if message.author != author:
                    return False
                try:
                    int(message.content)
                    return True
                except ValueError:
                    return False
            return inner_check

        try:
            await ctx.reply(f'(Respond with the number. You have 30 seconds)\nGet random quote from topic:\n```\n{res}```')
            answer = await self.bot.wait_for('message', check=check2, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.reply("You took too long, stupid slow human")

        await ctx.reply(f'Random result from topic: `{search_res[int(answer.content) - 1]}`'
                        f'\n\n```\n{random.choice(wikiquote.quotes(search_res[int(answer.content) - 1]))}```')

    @commands.command(name="dailyquote",
                      aliases=["qotd"],
                      description="Get the daily quote"
                      )
    async def _qotd(self, ctx):
        return await ctx.reply(f'{ctx.author.mention}\n{self.get_quotes()[0]}')

    @tasks.loop(minutes=1)
    async def daily_ping(self):
        await self.bot.wait_until_ready()

        for (key, value) in self.guilds.items():
            if datetime.now().hour == 8 and not value["sent"]:
                value["sent"] = True

                ping_role: discord.Role = self.bot.get_guild(
                    int(key)).get_role(value["role"])

                ping_channel: discord.TextChannel = self.bot.get_channel(value["channel"])

                quote: str = self.get_quotes()

                return await ping_channel.send("{0}\n```\n{1}```".format(ping_role.mention, quote))

            if datetime.now().hour != 8:
                value["sent"] = False

        self.quote_info.update("guilds", self.guilds)


def setup(bot):
    bot.add_cog(QuotesCommands(bot))
