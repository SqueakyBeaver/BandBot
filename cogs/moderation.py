import discord
from discord.ext import commands
import asyncio


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
        usage="[time (in minutes)] [\"reason\" (must have quotes if there is a space)] [user(s) (must be pings)]"
    )
    # @commands.has_role("Moderator")
    async def _mute(self, ctx, time: int, reason):
        success = 0
        already = 0

        users = [ctx.guild.get_member(id) for id in ctx.message.raw_mentions]

        muted = discord.utils.get(ctx.message.guild.roles, name="Muted")
        if (muted is None):
            muted = ctx.message.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                channel.set_permissions(muted, send_messages=False)

        for user in users:
            if muted in user.roles:
                already += 1
            else:
                success += 1
            await user.add_roles(muted, reason=reason)

        await ctx.send("{0} users muted.\n{1} users already muted."
                       "\nHave a nice day, muted people!!".format(success, already))

        await asyncio.sleep(time * 60)
        for user in users:
            await user.remove_roles(muted, reason="Mute timer up")


def setup(bot):
    bot.add_cog(ModerationCommands(bot))
