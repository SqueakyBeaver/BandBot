import io
import textwrap
import traceback
from contextlib import redirect_stdout

from discord.ext import commands


class DevCommands(commands.Cog, name="Developer Commands", command_attrs=dict(hidden=True)):
    """
    These are the developer commands
    """

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
            await ctx.send("Done")
        if cog in extensions:
            self.bot.unload_extension(cog)  # Unloads the cog
            self.bot.load_extension(cog)  # Loads the cog
            await ctx.send("Done")  # Sends a message where content="Done"
        else:
            await ctx.send("Unknown Cog")  # If the cog isn't found/loaded.

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
            await ctx.send("Cog is not loaded!")
            return
        self.bot.unload_extension(cog)
        await ctx.send("`{cog}` has successfully been unloaded.")

    @commands.command(
        name="load"
    )
    async def load(self, ctx, cog):
        """
        Loads a cog.
        """
        try:

            self.bot.load_extension(cog)
            await ctx.send(f"`{cog}` has successfully been loaded.")

        except commands.errors.ExtensionNotFound:
            await ctx.send(f"`{cog}` does not exist!")

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
        await ctx.send(base_string)

    def cleanup_code(self, content):
        """Cleanup for code block inputs"""

        content.replace("\'", "\\\'").replace("\"", "\\\"")

        if not content.startswith("```") or not content.endswith("```"):
            print("Not good")
            return {"blocked": False,
                    "res": f"You need code blocks, bud. Try \n```\`\`\`py\n{content}\n\`\`\`\n```"}

        content = content.replace("```", "\n```").strip()
        if content.startswith("```py\n"):
            return {"blocked": True,
            "res": "\n".join(content.split("\n")[1:-1])}

    @commands.check(commands.is_owner())
    @commands.command(hidden=True, name="eval")
    async def _eval(self, ctx, *, body: str):
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

        if not cleaned["blocked"]:
            return await ctx.send(cleaned["res"])

        body = cleaned["res"]

        stdout = io.StringIO()

        # to_compile = f"async def func():\n{textwrap.indent(body, '    ')}"
        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile.strip()+"\n", env)
        except Exception as e:
            print(e)
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}\n```")

        func = env["func"]
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f"```py\n{value}{traceback.format_exc()}\n```")
        else:
            value = stdout.getvalue()

            await ctx.message.add_reaction("\u2705")

            if value:
                await ctx.send(f"```py\n{value}\n```")


def setup(bot):
    bot.add_cog(DevCommands(bot))
