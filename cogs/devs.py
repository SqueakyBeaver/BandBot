import discord
from discord.ext import commands


class DevCommands(commands.Cog):
    '''These are the developer commands'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command(  # Decorator to declare where a command is.
        name='reload',  # Name of the command, defaults to function name.
        aliases=['rl'])
    async def reload(self, ctx, cog):
        '''
                Reloads a cog.
                '''
        if (await self.bot.is_owner(ctx.author)):
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

    @commands.command(name="unload",
                      aliases=['ul'])
    async def unload(self, ctx, cog):
        '''
                Unload a cog.
                '''
        if (await self.bot.is_owner(ctx.author)):
            extensions = self.bot.extensions
            if cog not in extensions:
                await ctx.send("Cog is not loaded!")
                return
            self.bot.unload_extension(cog)
            await ctx.send(f"`{cog}` has successfully been unloaded.")

    @commands.command(name="load")
    async def load(self, ctx, cog):
        '''
                Loads a cog.
                '''
        if (await self.bot.is_owner(ctx.author)):
            try:

                self.bot.load_extension(cog)
                await ctx.send(f"`{cog}` has successfully been loaded.")

            except commands.errors.ExtensionNotFound:
                await ctx.send(f"`{cog}` does not exist!")

    @commands.command(name="listcogs",
                      aliases=['lc'])
    async def listcogs(self, ctx):
        '''
                Returns a list of all enabled commands.
                '''
        if (await self.bot.is_owner(ctx.author)):
            # Gives some styling to the list (on pc side)
            base_string = "```css\n"
            base_string += "\n".join([str(cog) for cog in self.bot.extensions])
            base_string += "\n```"
            await ctx.send(base_string)


def setup(bot):
    bot.add_cog(DevCommands(bot))
