import urllib.parse
import aiohttp
import io

from discord.ext import flags, commands
import discord


class MiscCommands(commands.Cog, name="misc"):
    """Miscellaneous commands that I don't know where to put"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @flags.add_flag("--gif", type=bool, choices=[True, False], default=False)
    @flags.add_flag("--say", type=str, metavar="Text", default=None)
    @flags.add_flag("--filter", type=str, metavar="Filter", default=None)
    @flags.command(name="cat")
    async def _cat(self, ctx: commands.Context, **flags):
        """Get a random cat image"""
        async with ctx.typing():
            # /cat/gif/says/Hello?fi=filter
            link: str = "https://cataas.com/cat"
            link += "/gif" if flags["gif"] else ""
            link += "/says/{0}".format(urllib.parse.quote(
                flags["say"])) if flags["say"] else ""
            link += "?fi={0}".format(urllib.parse.quote(
                flags["filter"])) if flags["filter"] else ""

            e: discord.Embed = discord.Embed(
                title="Your cat, my good person", colour=discord.Colour.random())
            e.set_footer(text="requested by {0}#{1}".format(
                ctx.author.name, ctx.author.discriminator))
            e.set_image(url=link)

            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    if resp.status != 200:
                        return await ctx.reply('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await ctx.reply(content="Random cat from <https://cataas.com/cat>", file=discord.File(data, "a_cool_cat.{0}".format("gif" if flags["gif"] else "png")))

    @ commands.command(name="catsay", aliases=["catsays"])
    async def _cat_say(self, ctx: commands.Context, *, says: str=None):
        """Get a random cat image saying something"""
        e: discord.Embed=discord.Embed(
            title="Your cat, my good person", colour=discord.Colour.random())
        e.set_footer(text="requested by {0}#{1}".format(
            ctx.author.name, ctx.author.discriminator))
        e.set_image(
            url="https://cataas.com/c/s/{0}".format(urllib.parse.quote(says)))

        await ctx.reply(content="Random cat from <https://cataas.com/>",
                        embed=e)


def setup(bot: commands.Bot):
    bot.add_cog(MiscCommands(bot))
