import discord
from discord.ext import commands
from database import DBClient


class GeneralCommands(commands.Cog, name='General Commands'):
    """ General commands """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='ping',
        aliases=['poing']
    )
    async def ping(self, ctx):
        await ctx.send("{0} **PONG!**\nI took `{round(self.bot.latency * 1000)} ms` to respond".format(ctx.message.author.mention))

    @commands.command(
        name='feedback',
        aliases=['fb'],
        decription="Send feedback to the dev(s)")
    async def bug(self, ctx, *args):
        if (len(args) == 0):
            await ctx.send("Type `!fb <your feedback>`")
            return
        else:
            feedbackChannel = self.bot.get_channel(779738194097995806)
            await feedbackChannel.send("**FEEDBACK**\n{0} (**{1}#{2}**) says ```css\n{3}```"
                                       .format(ctx.author.id, ctx.message.author.name, ctx.message.author.discriminator, ' '.join(args)))
            await ctx.message.delete()
            await ctx.send("Thank you for that")


def setup(bot):
    bot.add_cog(GeneralCommands(bot))
