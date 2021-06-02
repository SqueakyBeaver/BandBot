import discord
from discord.ext import commands, tasks
from datetime import datetime
import pytz


class GeneralCommands(commands.Cog, name="general"):
    """ General commands """

    def __init__(self, bot):
        # bot.annoying_task = self.be_annoying.start()
        self.bot = bot

        # Channel: message
        self.deleted_messages: dict[discord.TextChannel, discord.Message] = {}

        # Channel: (before, after)
        self.edited_messages: dict[discord.TextChannel,
                                   tuple[discord.Message, discord.Message]] = {}

    @commands.command(
        name='ping',
        aliases=['poing']
    )
    async def ping(self, ctx: commands.Context):
        await ctx.reply(f'**PONG!**\nI took `{round(self.bot.latency * 1000)} ms` to respond')

    @commands.command(
        name='feedback',
        aliases=['fb'],
        decription="Send feedback to the dev(s)")
    async def bug(self, ctx: commands.Context, *args):
        if (len(args) == 0):
            await ctx.reply("Type `!fb <your feedback>`")
            return
        else:
            feedbackChannel = self.bot.get_channel(779738194097995806)
            await feedbackChannel.send(f'**FEEDBACK**\n{ctx.author.id} (**{ctx.message.author.name}#{ctx.message.author.discriminator}**) says ```css\n{" ".join(args)}```')
            await ctx.message.delete()
            await ctx.reply("Thank you for that")

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
            return await ctx.reply("There were no deletions that I could see.\n"
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

        await ctx.reply(ctx.author.mention, embed=embed)

    @snipe.command(name="edit")
    async def snipe_edit(self, ctx):
        if ctx.channel not in self.edited_messages:
            return await ctx.reply("There were no edits that I can see.\n"
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

        await ctx.reply(ctx.author.mention, embed=embed)

    @commands.command(name="newyear",
                      aliases=["endyear", "graduate"])
    async def new_year(self, ctx: commands.Context):
        guild: discord.Guild = ctx.guild
        roles = {"raisins": guild.get_role(827239098804469780), "senior": guild.get_role(769201494821306368), "junior": guild.get_role(769201510801211452),
                 "sophomore": guild.get_role(769201512227667999), "freshman": guild.get_role(769201513603137566), "middle school": guild.get_role(769201975346200606)}

        async with ctx.typing():
            for user in ctx.guild.members:
                if user.bot:
                    continue

                if roles["senior"] in user.roles:
                    await user.remove_roles(roles["senior"])
                    await user.add_roles(roles["raisins"])

                if roles["junior"] in user.roles:
                    await user.remove_roles(roles["junior"])
                    await user.add_roles(roles["senior"])

                if roles["sophomore"] in user.roles:
                    await user.remove_roles(roles["sophomore"])
                    await user.add_roles(roles["junior"])

                if roles["freshman"] in user.roles:
                    await user.remove_roles(roles["freshman"])
                    await user.add_roles(roles["sophomore"])

        await ctx.reply("Done")

def setup(bot):
    bot.add_cog(GeneralCommands(bot))
