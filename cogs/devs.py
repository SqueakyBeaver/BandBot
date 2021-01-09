import discord
from discord.ext import commands


class DevCommands(commands.Cog, name='Developer Commands', command_attrs=dict(hidden=True)):
    """
    These are the developer commands
    """

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        if (not await ctx.bot.is_owner(ctx.author)):
            raise commands.NotOwner("Nice try pal, but no")
        return True

    @commands.command(  # Decorator to declare where a command is.
        name='reload',  # Name of the command, defaults to function name.
        aliases=['rl']
    )
    async def reload(self, ctx, cog):
        """
        Reloads a cog.
        """
        # A list of the bot's cogs/extensions.
        extensions = self.bot.extensions
        if cog == 'all':  # Lets you reload all cogs at once
            for extension in extensions:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            await ctx.send('Done')
        if cog in extensions:
            self.bot.unload_extension(cog)  # Unloads the cog
            self.bot.load_extension(cog)  # Loads the cog
            await ctx.send('Done')  # Sends a message where content='Done'
        else:
            await ctx.send('Unknown Cog')  # If the cog isn't found/loaded.

    @commands.command(
        name="unload",
        aliases=['ul']
    )
    async def unload(self, ctx, cog):
        """
        Unload a cog.
        """
        extensions = self.bot.extensions
        if cog not in extensions:
            await ctx.send("Cog is not loaded!")
            return
        self.bot.unload_extension(cog)
        await ctx.send("`{0}` has successfully been unloaded.".format(cog))

    @commands.command(
        name="load"
    )
    async def load(self, ctx, cog):
        """
        Loads a cog.
        """
        try:

            self.bot.load_extension(cog)
            await ctx.send("`{0}` has successfully been loaded.".format(cog))

        except commands.errors.ExtensionNotFound:
            await ctx.send("`{0}` does not exist!".format(cog))

    @commands.command(
        name="listcogs",
        aliases=['lc']
    )
    async def listcogs(self, ctx):
        """
        Returns a list of all enabled commands.
        """
        # Gives some styling to the list (on pc side)
        base_string = "```css\n"
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n```"
        await ctx.send(base_string)


def setup(bot):
    bot.add_cog(DevCommands(bot))
