import discord
from discord.ext import commands
from utilities import Utilities


class GameNightCommands(commands.Cog):
    """Game Night Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='suggestgame',
                      aliases=['sg'],
                      description="Suggest a game for game night")
    async def suggest_game(self, ctx, *args):

        if (ctx.guild.id == 637316662801989658):
            suggestionChannel = self.bot.get_channel(744413784319328286)
        else:
            suggestionChannel = self.bot.get_channel(779541142818521108)

        suggestionAuthor = f'{ctx.author.name}#{ctx.author.discriminator}'

        await suggestionChannel.send(
            f"{ctx.message.author.id} (**{suggestionAuthor}**) suggested at {ctx.message.created_at}:```css\n{' '.join(args)}``` ")
        await ctx.message.delete()

    @commands.command(name="choosegame",
                      aliases=['cg', 'game'],
                      description="Accept a game for game night",
                      )
    async def choose_game(self, ctx, messageID):
        if (not await self.bot.is_owner(ctx.message.author)):
            print(ctx.message.author.id)
            await ctx.send("No")
            return

        if (ctx.guild.id == 637316662801989658):
            acceptRole = ctx.guild.get_role(732078243875651677)
            pingRole = ctx.guild.default_role
            announcementChannel = self.bot.get_channel(
                637316663267819561)
        else:
            acceptRole = ctx.guild.get_role(767859838654742568) #Remember to change this later
            pingRole = ctx.guild.get_role(779749274773749870)
            announcementChannel = self.bot.get_channel(
                779541190252298270)

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

                await announcementChannel.send(f"{pingRole.mention}\nWe will play {await Utilities.get_content(ctx, self, messageID)}")
            except:
                await ctx.send("Either you did something stupid or I messed up.\nIf you think you did nothing wrong, type b!bug")
                return


def setup(bot):
    bot.add_cog(GameNightCommands(bot))
