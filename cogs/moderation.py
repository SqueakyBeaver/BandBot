from xml.etree.ElementTree import TreeBuilder
import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime
import dateparser


class Checks():
    def is_author(author):
        def inner_check(message):
            return message.author == author
        return inner_check

    def is_author_channel(author):
        def inner_check(message):
            return message.author == author and message.raw_channel_mentions
        return inner_check


class ModerationCommands(commands.Cog, name="moderation"):
    """ Commands for moderators to be used by moderators """

    def __init__(self, bot):
        self.bot = bot
        self.tasks = []

    # hoices: List of choices
    # res: Dictionary of results same size as choices
    # check: Function used to check if the response meets a requirement
    async def choose(self, ctx, choices, res, check=Checks.is_author):
        try:
            for i in choices:
                await ctx.send(i)
                answer = await self.bot.wait_for('message', check=check, timeout=30)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long, stupid slow human")
        if res[answer]:
            return res[answer]

    async def task(self, end, func_end, *args, **kwargs):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            print(end - datetime.now())
            if datetime.now() >= end:
                return await func_end(*args, **kwargs)
            else:
                await asyncio.sleep(3)

    async def bulk_delete(self, channel: discord.TextChannel, user_ids, limit=100):
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
        name='lock',
        description="Lock something",
    )
    # @commands.has_role("Moderator")
    async def _lock(self, ctx, *, dest: str):
        channels = {}
        everyone = ctx.guild.default_role
        perms = everyone.permissions
        perms.send_messages = False

        for i in ctx.guild.text_channels:
            channels[i.id] = i

        async def server():
            await everyone.edit(permissions=perms)
            await ctx.send("Server locked")

        async def channel():
            await ctx.channel.set_permissions(everyone, send_messages=False)

            # Later
            # self.choose(ctx, ["Which channel?"], channels, Checks.is_author_channel)
        if "channel" in dest.lower():
            await channel()
            return await ctx.send("Locked")
        if "server" in dest.lower():
            await server()
            return await ctx.send("Locked")

        await ctx.send("Invalid option. Options are: **`Server`** or **`Channel`**")

    @commands.command(
        name="unlock",
        description="Unlock something",
    )
    # @commands.has_role("Moderator")
    async def _unlock(self, ctx, dest):
        channels = {}
        everyone = ctx.guild.default_role
        perms = everyone.permissions
        perms.send_messages = True

        for i in ctx.guild.text_channels:
            channels[i.id] = i

        async def server():
            await everyone.edit(permissions=perms)

        async def channel():
            await ctx.channel.set_permissions(everyone, send_messages=None)

            # Later
            # self.choose(ctx, ["Which channel?"], channels, Checks.is_author_channel)
        if "channel" in dest.lower():
            await channel()
            return await ctx.send("Unlocked")
        if "server" in dest.lower():
            await server()
            return await ctx.send("Unlocked")

        await ctx.send("Invalid option. Options are: **`Server`** or **`Channel`**")

    @commands.command(
        name="mute",
        description="Mute person or people for given amount of minutes",
        usage="[time (in minutes)] [user]"
    )
    @commands.has_role("Moderator")
    async def _mute(self, ctx, time: str, *, mentions):
        users = ctx.message.raw_mentions

        end_time = dateparser.parse("in " + time)
        if not end_time or end_time < datetime.now():
            return await ctx.send("Invalid time!")

        muted = discord.utils.get(ctx.message.guild.roles, name="Muted")
        if (muted is None):
            muted = await ctx.message.guild.create_role(name="Muted")
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted, send_messages=False)

        for id in users:
            user = ctx.guild.get_member(id)
            if not muted in user.roles:
                await ctx.send(f'{user.mention} was muted for {time}')
            else:
                return await ctx.send(f'{user.mention} is already muted/cannot be muted')
            await user.add_roles(muted)

        async def __unmute(guild, users):
            for id in users:
                user = guild.get_member(id)
                await user.remove_roles(muted, reason="Mute timer up")
                await user.send("You have been unmuted!")

        self.tasks.append(self.bot.loop.create_task(
            self.task(end_time, __unmute, guild=ctx.guild, users=users)))

    @commands.command(
        name="unmute",
        description="Unmute a person",
        usage="[user]"
    )
    async def _unmute(self, ctx, user):
        muted = discord.utils.get(ctx.message.guild.roles, name="Muted")

        users = ctx.message.raw_mentions

        for id in users:
            user = ctx.guild.get_member(id)
            if muted in user.roles:
                await user.remove_roles(muted, reason="Unmured")
                await ctx.send(f'{user.mention} was unmuted')
            else:
                await ctx.send(f'{user.mention} is not muted')


def setup(bot):
    bot.add_cog(ModerationCommands(bot))
