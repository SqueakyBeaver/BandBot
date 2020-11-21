import discord
from discord.ext import commands


class GeneralCommands(commands.Cog):
    """ General commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', aliases=['poing'])
    async def ping(self, ctx):
        await ctx.send(f"{ctx.message.author.mention} **PONG!**\nI took `{round(self.bot.latency * 1000)} ms` to respond")

    @commands.command(name='feedback', aliases=['complain', 'compliment', 'suggest'], hidden=True)
    async def feedback(self, ctx, *args):
        feedbackChannel = self.bot.get_channel(779738194097995806)
        await feedbackChannel.send(f"{ctx.author.id} (**{ctx.message.author.name}#{ctx.message.author.discriminator}**) says ```css\n{' '.join(args)}```")
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(GeneralCommands(bot))
