import discord
from discord.ext import commands

class GeneralCommands(commands.Cogs):
    """ General commands """

    def __init__(self,bot):
        self.bot = bot

    @commands.command(name='ping', aliases=['poing'])
    async def ping(self, ctx):
        await ctx.send(f"{ctx.message.author.mention} PONG!\nI took {self.bot.latency * 1000} ms to respond")

    @commands.command(name='feedback', aliases=['complain', 'compliment', 'suggest'])
    async def feedback(self, ctx, *args):
        await self.bot.owner.dm_channel.send(f"**{ctx.message.author.discriminator}** says ```css{' '.join(args)}```")
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(GeneralCommands(bot))
