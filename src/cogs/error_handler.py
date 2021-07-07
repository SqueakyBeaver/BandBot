import discord
import traceback
import sys
import inspect
from discord.ext import commands


class CommandErrorHandler(commands.Cog, name="Error handler"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        await ctx.send("**TESTING**")
        if hasattr(ctx.command, "on_error"):
            return

        cog = ctx.cog
        if cog and cog._get_overridden_method(cog.cog_command_error) is not None:
            return

        ignored = (commands.CommandNotFound,)
        error = getattr(error, "original", error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f"{ctx.command} has been disabled.")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(
                    f"{ctx.command} can not be used in Private Messages."
                )
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingRole):
            await ctx.send("You do not have the necessary role to use this command.")

        elif isinstance(error, commands.BadArgument):
            # if ctx.command.qualified_name == 'tag list':
            await ctx.send("I could not find that member. Please try again.")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "Missing parameter(s) for command {0}:\n```py\n{1}={2}```".format(
                    ctx.command,
                    error.param,
                    error.param.default
                    if error.param.default != inspect.Parameter.empty
                    else None,
                )
            )

        elif isinstance(error, commands.ArgumentParsingError):
            await ctx.send(
                "Incorrect usage\n The usage for {0} is ```py\n{1}```".format(
                    ctx.command, "\n".join([i for _, i in ctx.command.clean_params])
                )
            )

        else:
            print(
                "Ignoring exception in command {}:".format(ctx.command), file=sys.stderr
            )
            traceback.print_exception(
                type(error), error, error.__traceback__, file=sys.stderr
            )


def setup(bot: commands.Bot):
    bot.add_cog(CommandErrorHandler(bot))
