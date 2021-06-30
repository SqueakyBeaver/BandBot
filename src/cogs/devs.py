import io
import textwrap
import traceback
import logging
from contextlib import redirect_stdout

from discord.ext import commands


class DevCommands(commands.Cog, name="developer", command_attrs=dict(hidden=True)):
    """ Developer commands """

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    async def cog_check(self, ctx):
        if (not await ctx.bot.is_owner(ctx.author)):
            raise commands.NotOwner("Nice try pal, but no")
        return True

    @commands.command(  # Decorator to declare where a command is.
        name="reload",  # Name of the command, defaults to function name.
        aliases=["rl"]
    )
    async def reload(self, ctx, cog):
        """
        Reloads a cog.
        """
        # A list of the bot's cogs/extensions.
        extensions = self.bot.extensions
        if cog == "all":  # Lets you reload all cogs at once
            for extension in extensions:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            await ctx.reply("Done")
        if cog in extensions:
            self.bot.unload_extension(cog)  # Unloads the cog
            self.bot.load_extension(cog)  # Loads the cog
            await ctx.reply("Done")  # Sends a message where content="Done"
        else:
            await ctx.reply("Unknown Cog")  # If the cog isn't found/loaded.

    @commands.command(
        name="unload",
        aliases=["ul"]
    )
    async def unload(self, ctx, cog):
        """
        Unload a cog.
        """
        extensions = self.bot.extensions
        if cog not in extensions:
            await ctx.reply("Cog is not loaded!")
            return
        self.bot.unload_extension(cog)
        await ctx.reply("`{cog}` has successfully been unloaded.")

    @commands.command(
        name="load"
    )
    async def load(self, ctx, cog):
        """
        Loads a cog.
        """
        try:

            self.bot.load_extension(cog)
            await ctx.reply(f"`{cog}` has successfully been loaded.")

        except commands.errors.ExtensionNotFound:
            await ctx.reply(f"`{cog}` does not exist!")

    @commands.command(
        name="listcogs",
        aliases=["lc"]
    )
    async def listcogs(self, ctx):
        """
        Returns a list of all enabled commands.
        """
        # Gives some styling to the list (on pc side)
        base_string = "```css\n"
        base_string += "\n".join([str(cog) for cog in self.bot.extensions])
        base_string += "\n```"
        await ctx.reply(base_string)

    def cleanup_code(self, content):
        """Cleanup for code block inputs"""

        content.replace("\'", "\\\'").replace("\"", "\\\"")

        if not content.startswith("```") or not content.endswith("```"):
            logging.warning("Not good")
            return {"blocks": False,
                    "res": f"You need code blocks. Try \n\`\`\`py\n{content}\n\`\`\`\n"}

        content = content.replace("```", "\n```").strip()
        if content.startswith("```py\n"):
            return {"blocks": True,
                    "res": "\n".join(content.split("\n")[1:-1])}

    @commands.check(commands.is_owner())
    @commands.command(hidden=True, name="eval")
    async def _eval(self, ctx,  body: str):
        """Evaluates code"""

        env = {
            "bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "_": self._last_result
        }

        env.update(globals())

        cleaned = self.cleanup_code(body)

        if not cleaned["blocks"]:
            return await ctx.reply(cleaned["res"])

        body = cleaned["res"]

        stdout = io.StringIO()

        to_compile = f"async def func():\n{textwrap.indent(body, '    ')}"

        try:
            exec(to_compile, env)
        except Exception as e:
            logging.error(e)
            return await ctx.reply(f"```py\n{e.__class__.__name__}: {e}\n```")

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.reply(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()

            await ctx.message.add_reaction("\u2705")

            if value:
                await ctx.reply(f"```py\n{value}\n```")


def setup(bot):
    bot.add_cog(DevCommands(bot))
