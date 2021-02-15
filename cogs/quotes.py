from discord.ext import commands, tasks
from database import DBClient
from datetime import datetime

import asyncio
import discord
import wikiquote
import random


reminderDB = DBClient("dailyReminder")


class QuotesCommands(commands.Cog, name='Quote Commands'):

    def __init__(self, bot):
        bot.bg_task = self.daily_ping.start()
        self.pinged = False
        self.bot: commands.Bot = bot

    @commands.command(name='joinping',
                      aliases=['jp'],
                      description="Join the daily quote ping")
    async def join_reminder(self, ctx):
        if (reminderDB.find(ctx.message.author.id) is None):
            reminderDB.add_ping(ctx.message.author.id)
            await ctx.send("Successfully joined the daily quote ping")
        else:
            await ctx.send("You're already in the daily quote ping..")

    @commands.command(name='leaveping',
                      aliases=['lp'],
                      description="Leave the daily quote pinging because you don't like pings")
    async def leave_ping(self, ctx):
        if (reminderDB.find(ctx.message.author.id) is not None):
            reminderDB.delete({"_id": ctx.message.author.id})
            await ctx.send("Hope you like your ping-free life")
        else:
            await ctx.send("You can't leave something you never joined")

    @commands.command(
        name="quote",
        description="Random quote from WikiQuote",
        usage="quote [search]"
    )
    async def _quote(self, ctx, *query):
        if ' '.join(query):
            res = wikiquote.quotes(random.choice(
                wikiquote.search(' '.join(query).strip())))
            if not res:
                return await ctx.send(f'No quotes from {" ".join(query).strip()}')
            return await ctx.send(f'```\n{res[0]}\n~{" ".join(query).strip()}```')

        def check(author):
            def inner_check(message):
                return message.author == author
            return inner_check

        try:
            await ctx.send("Would you like a random quote? `Yes/No`\nYou have 30 seconds to respond")
            answer = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long, stupid slow human")


        if "y" in answer.content.lower():
            author = random.choice(wikiquote.random_titles())
            res = random.choice(wikiquote.quotes(author))
            return await ctx.send(f'```\n{res}\n~{author}```')
        elif not "n" in answer.content.lower():
            return await ctx.send("Invalid choice!")

        try:
            await ctx.send("What would you like to search for? \nYou have 30 seconds to respond")
            answer = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long, stupid slow human")

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
            await ctx.send(f'(Respond with the number. You have 30 seconds)\nGet random quote from topic:\n```\n{res}```')
            answer = await self.bot.wait_for('message', check=check2, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long, stupid slow human")

        await ctx.send(f'Random result from topic: `{search_res[int(answer.content) - 1]}`'
                       f'\n\n```\n{random.choice(wikiquote.quotes(search_res[int(answer.content) - 1]))}```')

    def get_quotes(self):
        daily_quote = wikiquote.quote_of_the_day()
        return (f'{daily_quote[0]}\n~{daily_quote[1]}',
                f'{random.choice(wikiquote.quotes("Linus Torvalds"))}\n ~Linus Torvalds')

    @tasks.loop(minutes=1)
    async def daily_ping(self):
        await self.bot.wait_until_ready()

        ping_channel = self.bot.get_channel(767858104066637834)

        if datetime.now().hour == 8 and not self.pinged:
            self.pinged = True
            pingUsers = reminderDB.dataset.find({})
            pingStr = ""
            quotes = self.get_quotes()

            for userID in pingUsers:
                user = ping_channel.guild.get_member(userID["_id"])
                pingStr += f'{user.mention}'

            await ping_channel.send(f'{pingStr}\n```\n{quotes[0]}```')
            await ping_channel.send(f'Also,\n```\n{quotes[1]}```')

        if datetime.now().hour != 8:
            self.pinged = False


def setup(bot):
    bot.add_cog(QuotesCommands(bot))
