from cogs.general import GeneralCommands
import discord
from discord.ext import commands
import pytz
from datetime import datetime


class SnipeCommands(commands.Cog, name="sniping", command_attrs=dict(cog_name="general")):
    """Snipe a deletion or edit"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # Channel: message
        self.deleted_messages: dict[discord.TextChannel, discord.Message] = {}

        # Channel: (before, after)
        self.edited_messages: dict[discord.TextChannel,
                                   tuple[discord.Message, discord.Message]] = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        self.deleted_messages[message.channel] = message

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        self.edited_messages[before.channel] = (before, after)

    @commands.group(name="snipe",
                    description="Snipe an edit or deletion",
                    usage="[delete|edit]\nDefaults to delete if no argument is provided"
                    )
    async def snipe(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await self.snipe_deletion(ctx)

    @snipe.command(name="deletion",
                   aliases=["delete"])
    async def snipe_deletion(self, ctx: commands.Context):
        if ctx.channel not in self.deleted_messages:
            return await ctx.send("There were no deletions that I could see.\n"
                                  "Better luck next time.")

        embed: discord.Embed = discord.Embed(colour=discord.Colour.green(),
                                             title="I found that filthy deleter")
        message: discord.Message = self.deleted_messages[ctx.channel]

        embed.add_field(name="Deleted message:\n", value=message.content)
        embed.add_field(name="\nAuthor:\n", value="{0}#{1}".format(
            message.author.display_name, message.author.discriminator))

        embed.set_footer(text="Requested by: {0}#{1} | {2}".format(ctx.author.display_name,
                                                                   ctx.author.discriminator, datetime.strftime(datetime.now(pytz.timezone("US/Central")), "%H:%M:%S")),
                         icon_url="https://i.redd.it/k9wl9ypumyp31.png")

        await ctx.send(ctx.author.mention, embed=embed)

    @snipe.command(name="edit")
    async def snipe_edit(self, ctx):
        if ctx.channel not in self.edited_messages:
            return await ctx.send("There were no edits that I can see.\n"
                                  "Better luck next time.")

        embed: discord.Embed = discord.Embed(colour=discord.Colour.green(),
                                             title="I see what they tried to hide")

        # (Before, After)
        edit: tuple[discord.Message,
                    discord.Message] = self.edited_messages[ctx.channel]

        embed.add_field(name="Before:\n", value=edit[0].content)
        embed.add_field(name="\nAfter:\n", value=edit[1].content)
        embed.add_field(name="\nAuthor:\n", value="{0}#{1}".format(
            edit[0].author.display_name, edit[0].author.discriminator))

        embed.set_footer(text="Requested by: {0}#{1} | {2}".format(ctx.author.display_name,
                                                                   ctx.author.discriminator, datetime.strftime(datetime.now(pytz.timezone("US/Central")), "%H:%M:%S")),
                         icon_url="https://i.redd.it/k9wl9ypumyp31.png")

        await ctx.send(ctx.author.mention, embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(SnipeCommands(bot))
