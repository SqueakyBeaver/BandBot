import discord
from discord.ext import commands


class ModerationCommands(commands.Cog, name='Moderation Commands'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='purge',
                      decription="Bulk delete messages"
                      )
    @commands.has_role('Moderator')
    async def mass_delete(self, ctx, amount=100):
        await ctx.channel.purge(limit=amount)

    @commands.command(name='lockserver',
                      description="Lock the server",
                      aliases=['serverlock', 'ls', 'sl']
                      )
    @commands.has_role('Moderator')
    async def lock_server(self, ctx):
        role = ctx.guild.default_role
        perms = role.permissions
        perms.send_messages = False
        await role.edit(permissions=perms)
        await ctx.send("Server locked")

    @commands.command(name='unlockserver',
                      description="Unlock the server",
                      aliases=['serverunlock', 'us', 'su']
                      )
    @commands.has_role('Moderator')
    async def unlock_server(self, ctx):
        role = ctx.guild.default_role
        perms = role.permissions
        perms.send_messages = True
        await role.edit(permissions=perms)
        await ctx.send("Server unlocked")

def setup(bot):
    bot.add_cog(ModerationCommands(bot))
