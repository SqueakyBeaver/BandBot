import discord
from discord.ext import commands
from utilities import Utilities
from database import DBClient


class GameNightCommands(commands.Cog, name="Game Night Commands"):
    """Game Night Commands"""

    def __init__(self, bot):
        self.bot = bot
        self.suggestionDB = DBClient("gameIdeas")

    @commands.command(name='suggestgame',
                      aliases=['sg'],
                      description="Suggest a game for game night")
    async def suggest_game(self, ctx, *args):

        if (ctx.guild.id == 637316662801989658):
            decisionChannel = self.bot.get_channel(744413784319328286)
        else:
            decisionChannel = self.bot.get_channel(779541142818521108)

        suggestionAuthor = f'{ctx.author.name}#{ctx.author.discriminator}'
        suggestionID = self.suggestionDB.add(
            ctx.author.id, ' '.join(args))

        reactionTo = await decisionChannel.send(
            f"Suggestion number {suggestionID}\n**{suggestionAuthor}** suggested at `{ctx.message.created_at}`:```css\n{' '.join(args)}``` ")
        await reactionTo.add_reaction('👍')
        await reactionTo.add_reaction('👎')

        await ctx.message.delete()

    @commands.command(name="choosegame",
                      aliases=['cg', 'game'],
                      description="Accept a game for game night",
                      )
    async def choose_game(self, ctx, suggestionID, time="7:00 PM", day="Saturday"):
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
            # Remember to change this later
            acceptRole = ctx.guild.get_role(767859838654742568)
            pingRole = ctx.guild.get_role(779749274773749870)
            announcementChannel = self.bot.get_channel(
                779541190252298270)

        if (acceptRole in ctx.author.roles):
            # try:
            acceptedInfo = self.suggestionDB.find({'_id': int(suggestionID)})
            acceptedAuthor = ctx.guild.get_member(acceptedInfo['author'])
            acceptedContent = acceptedInfo['content']

            if (acceptedAuthor.dm_channel is None):
                await acceptedAuthor.create_dm()
                await acceptedAuthor.dm_channel.send(
                    f"Congratulations! Your suggestion {acceptedContent} was accepted!")
            else:
                await acceptedAuthor.dm_channel.send(
                    f"Congratulations! Your suggestion {acceptedContent} was accepted!")

            await announcementChannel.send(f"{pingRole.mention}\nWe will play ```css\n{acceptedContent}```"
                                           f"this {day} at {time}\n\nSuggested by {acceptedAuthor.mention}")

            await ctx.message.delete()

            # except:
            #    await ctx.send("Either you did something stupid or I messed up.\nIf you think you did nothing wrong, type b!bug")
            #    return

    @commands.command(name='join',
                      description="Join game night role and pings")
    async def join_game_night(self, ctx):
        if (ctx.guild.get_role(779749274773749870) in ctx.author.roles):
            await ctx.send("Stop trying to break me")
            return
        else:
            try:
                await ctx.author.add_roles(discord.Object(779749274773749870), reason="This is a cool person")
                await ctx.send("Success!")
            except:
                await ctx.send("Something went wrong. Either do the thing right or type `b!bug`")

    @commands.command(name='leave',
                      description='Leave the game night role')
    @commands.has_role(779749274773749870)
    async def leave_game_night(self, ctx):
        if (ctx.channel.id == 779541142818521108):
            await ctx.message.delete()
        try:
            await ctx.author.remove_roles(discord.Object(779749274773749870), reason="Doesn't like ping, I guess")
            await ctx.send("Success")
        except:
            await ctx.send("Something went wrong. Either do the thing right or type `b!bug`")

    @commands.command(name='resetsuggestions',
                      aliases=['reset', 'rs'],
                      hidden=True,
                      description="Reset suggestion counter to 1")
    async def reset_suggestions(self, ctx):
        if (await self.bot.is_owner(ctx.author)):
            if (ctx.guild.id == 637316662801989658):
                decisionChannel = self.bot.get_channel(744413784319328286)
            else:
                decisionChannel = self.bot.get_channel(779541142818521108)

            decisionChannel.purge(99999999999999999)
            self.suggestionDB.clear()
            with open("suggestionID.txt", 'w') as f:
                f.write("1\n")
                await ctx.send("Reset suggestions")


def setup(bot):
    bot.add_cog(GameNightCommands(bot))
