from discord.ext import commands
import discord


class MiscCommands(commands.Cog, name="misc"):
    """Miscellaneous commands that I don't know where to put"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="cat")
    async def _cat(self, ctx: commands.Context):
        """Get a random cat image"""
        e: discord.Embed = discord.Embed(title="Your cat, my good person", colour=discord.Colour.random(
        )).set_footer(text="requested by {0}\#{1}".format(ctx.author.name, ctx.author.discriminator)).set_image(url="https://cataas.com/c")

        await ctx.reply(content="Random cat from <https://cataas.com/>",
                        embed=e)


def setup(bot: commands.Bot):
    bot.add_cog(MiscCommands(bot))
