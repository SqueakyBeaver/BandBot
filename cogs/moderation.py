import discord
from discord.ext import commands
import asyncio

from discord.ext.commands.core import has_role


class ModerationCommands(commands.Cog, name='Moderation Commands'):
    purgeUsers = []

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if (not commands.has_role("Moderator")):
            raise commands.MissingRole("You are not a moderator, bud")
        return True

    async def will_purge(message):
        return message.author in ModerationCommands.purgeUsers

    @commands.command(
        name='purge',
        decription="Bulk delete messages",
        usage="b!purge [amount=100] <user(s)>"
    )
    # @commands.has_role("Moderator")
    async def mass_delete(self, ctx, amount=100):
        mentionedIDs = ctx.message.raw_mentions
        self.purgeUsers = [ctx.guild.get_member(user) for user in mentionedIDs]
        await ctx.message.delete()
        await ctx.channel.purge(check=ModerationCommands.will_purge, limit=amount)
        await ctx.send("Done.", delete_after=3)

    @commands.command(
        name='lockserver',
        description="Lock the server",
        aliases=['serverlock', 'ls', 'sl']
    )
    # @commands.has_role("Moderator")
    async def lock_server(self, ctx):
        role = ctx.guild.default_role
        perms = role.permissions
        perms.send_messages = False
        await role.edit(permissions=perms)
        await ctx.send("Server locked")

    @commands.command(
        name='unlockserver',
        description="Unlock the server",
        aliases=['serverunlock', 'us', 'su']
    )
    # @commands.has_role("Moderator")
    async def unlock_server(self, ctx):
        role = ctx.guild.default_role
        perms = role.permissions
        perms.send_messages = True
        await role.edit(permissions=perms)
        await ctx.send("Server unlocked")

    @commands.command(
        name="mute",
        description="Mute person or people for given amount of minutes",
        usage="[time (in minutes)] [user]"
    )
    @commands.has_role("Moderator")
    async def _mute(self, ctx, time: int, user):
        success = 0
        already = 0

        muted = discord.utils.get(ctx.message.guild.roles, name="Muted")
        if (muted is None):
            muted = ctx.message.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                channel.set_permissions(muted, send_messages=False)

        if muted in user.roles:
            await ctx.send("{0} was muted".format(user.mention))
        else:
            await ctx.send("{0} is already muted/cannot be muted".format(user.mention))
        await user.add_roles(muted)

        await asyncio.sleep(time * 60)
        await user.remove_roles(muted, reason="Mute timer up")

    @commands.command(
        name="unmute",
        description="Unmute a person",
        usage="[user]"
    )
    async def _unmute(self, ctx, user):
        muted = discord.utils.get(ctx.message.guild.roles, name="Muted")
        if user.has_role(muted):
            await user.remove_roles(muted, reason="Unmured")
            await ctx.send("{0} was unmuted".format(user.mention))
        else:
            await ctx.send("{0} is not muted".format(user.mention))


def setup(bot):
    bot.add_cog(ModerationCommands(bot))
