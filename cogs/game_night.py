import discord
from discord.ext import commands
from utilities import Utilities


class GameNightCommands(commands.Cog):
    """Game Night Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='suggestgame', aliases=['sg'])
    async def suggest_game(self, ctx, *args):
        suggestionChannel = self.bot.get_channel(744413784319328286)
        suggestionAuthor = f'{ctx.author.name}#{ctx.author.discriminator}'

        await suggestionChannel.send(
            f"{ctx.message.author.id} (**{suggestionAuthor}**) suggested at {ctx.message.created_at}:```css\n{' '.join(args)}``` ")
        await ctx.message.delete()

    @commands.command(name="choosegame", aliases=['cg', 'game'])
    async def choose_game(self, ctx, messageID):
        acceptRole = ctx.guild.get_role(732078243875651677)
        if (acceptRole in ctx.author.roles):
            try:
                notifyUser = await Utilities.get_user(ctx, self, messageID)


                if (notifyUser.dm_channel is None):
                    await notifyUser.create_dm()
                    await notifyUser.dm_channel.send(
                        f"Congratulations! Your suggestion {await Utilities.get_content(ctx, self, messageID)} was accepted!")
                else:
                    await notifyUser.dm_channel.send(
                        f"Congratulations! Your suggestion {await Utilities.get_content(ctx, self, messageID)} was accepted!")

                announcementChannel = self.bot.get_channel(637316663267819561)
                await announcementChannel.send(f"We will play {await Utilities.get_content(ctx, self, messageID)} {ctx.guild.default_role}")
            except:
                await ctx.send("Either you did something stupid or I messed up.\nIf you think you did nothing wrong, type b!bug")
                return


def setup(bot):
    bot.add_cog(GameNightCommands(bot))
