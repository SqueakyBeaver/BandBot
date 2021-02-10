import discord
from discord.ext import commands
import asyncio


class ModerationCommands(commands.Cog, name='Moderation Commands'):
    def __init__(self, bot):
        self.bot = bot


    async def bulk_delete(self, channel: discord.TextChannel, user_ids, limit = 100):
        delete_list = []
        count = 0
        try:
            async for message in channel.history(limit=100):
                if message.author.id in user_ids and count < limit:
                    delete_list.append(message)
                    count += 1
            await channel.delete_messages(delete_list)
        except Exception as e:
            return f'```py\n{e}\n```'
        return f'Successfully purged {len(delete_list)} messages.'

    @commands.command(
        name='purge',
        decription="Bulk delete messages",
        usage="b!purge [amount=100] <user(s)>"
    )
    @commands.has_permissions(manage_messages=True)
    async def _purge(self, ctx, amount=100):
        wait_message = await ctx.send("Working, please allow some time.")
        async with ctx.channel.typing():
            mentionedIDs = ctx.message.raw_mentions
            await ctx.message.delete()
            ret_str = await self.bulk_delete(ctx.channel, mentionedIDs, amount)
        await wait_message.edit(content=ret_str)

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
