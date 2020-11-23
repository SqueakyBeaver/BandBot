import discord
from discord.ext import commands
from database import DBClient


class GeneralCommands(commands.Cog):
    """ General commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping',
                      aliases=['poing']
                      )
    async def ping(self, ctx):
        await ctx.send(f"{ctx.message.author.mention} **PONG!**\nI took `{round(self.bot.latency * 1000)} ms` to respond")

    @commands.command(name='feedback', aliases=['complain', 'compliment', 'suggest'], hidden=True)
    async def feedback(self, ctx, *args):
        if (not await self.bot.is_owner(ctx.message.author)):
            feedbackChannel = self.bot.get_channel(779738194097995806)
            await feedbackChannel.send(f"{ctx.author.id} (**{ctx.message.author.name}#{ctx.message.author.discriminator}**) says ```css\n{' '.join(args)}```")
            await ctx.message.delete()

    @commands.command(name='purge',
                      decription="Bulk delete messages"
                      )
    @commands.has_permissions(manage_messages=True)
    async def mass_delete(self, ctx, amount=100):
        await ctx.channel.purge(limit=amount)

    @commands.command(name='bug',
                      aliases=['report', 'bugreport', 'br'],
                      decription="Send a bug report")
    async def bug(self, ctx, *args):
        if (len(args) == 0):
            await ctx.send("Type `!bug <bug you encountered>`")
            return
        else:
            feedbackChannel = self.bot.get_channel(779738194097995806)
            await feedbackChannel.send(f"**BUG REPORT**\n{ctx.author.id} (**{ctx.message.author.name}#{ctx.message.author.discriminator}**) says ```css\n{' '.join(args)}```")
            await ctx.message.delete()
            await ctx.send("Thank you for that")


def setup(bot):
    bot.add_cog(GeneralCommands(bot))
