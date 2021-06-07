import discord
import logging
from discord.ext import commands
from utilities import SuggestUtilities
from database import DBClient


class GameNightCommands(commands.Cog, name="game night"):
    """ Game Night Commands """

    def __init__(self, bot):
        self.bot = bot
        self.suggestionDB: DBClient = DBClient("gameIdeas")

    @commands.command(
        name='suggestgame',
        aliases=['sg'],
        description="Suggest a game for game night"
    )
    async def suggest_game(self, ctx, *, args: str):

        if (ctx.guild.id == 637316662801989658):
            decisionChannel = self.bot.get_channel(744413784319328286)
        else:
            decisionChannel = self.bot.get_channel(779541142818521108)

        suggestionAuthor = f'{ctx.author.name}#{ctx.author.discriminator}'
        suggestionID = self.suggestionDB.add_suggestion(
            ctx.author.id, args)

        reactionTo = await decisionChannel.send(
            f'Suggestion number {suggestionID}\n**{suggestionAuthor}** suggested at `{ctx.message.created_at}`:```css\n{ctx.message.created_at}``` ')
        await reactionTo.add_reaction('👍')
        await reactionTo.add_reaction('👎')

        await ctx.message.delete()

    @commands.command(
        name="choosegame",
        aliases=['cg', 'game'],
        description="Accept a game for game night",
    )
    async def choose_game(self, ctx, suggestionID: int, time: str = "7:00 PM", day: str = "Saturday"):
        if (not await self.bot.is_owner(ctx.message.author)):
            logging.info(ctx.message.author.id)
            await ctx.reply("No")
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
            DB_data = self.suggestionDB.find('id', int(suggestionID))

            for i in DB_data:
                if "suggestions" in i.keys():
                    accepted_info = i
                    break

            accepted_author = ctx.guild.get_member(accepted_info['author'])
            accepted_content = accepted_info['content']

            if (accepted_author.dm_channel is None):
                await accepted_author.create_dm()
                await accepted_author.dm_channel.send(
                    f'Congratulations! Your suggestion {accepted_content} was accepted!')
            else:
                await accepted_author.dm_channel.send(
                    f'Congratulations! Your suggestion {accepted_content} was accepted!')

            await announcementChannel.send(f'{pingRole.mention}\nWe will play ```css\n{accepted_content}``` this {day} at {time}\n\nSuggested by {accepted_author.mention}')

            await ctx.message.delete()

            # except:
            #    await ctx.reply("Either you did something stupid or I messed up.\nIf you think you did nothing wrong, type b!bug")
            #    return

    @ commands.command(
        name='join',
        description="Join game night role and pings"
    )
    async def join_game_night(self, ctx):
        if (ctx.guild.get_role(779749274773749870) in ctx.author.roles):
            await ctx.reply("Stop trying to break me")
            return
        else:
            try:
                await ctx.author.add_roles(discord.Object(779749274773749870), reason="This is a cool person")
                await ctx.reply("Success!")
            except:
                await ctx.reply("Something went wrong. Either do the thing right or type `b!bug`")

    @ commands.command(
        name='leave',
        description="Leave the game night role"
    )
    @ commands.has_role(779749274773749870)
    async def leave_game_night(self, ctx):
        if (ctx.channel.id == 779541142818521108):
            await ctx.message.delete()
        try:
            await ctx.author.remove_roles(discord.Object(779749274773749870), reason="Doesn't like ping, I guess")
            await ctx.reply("Success")
        except:
            await ctx.reply("Something went wrong. Either do the thing right or type `b!bug`")

    @ commands.command(
        name='resetsuggestions',
        aliases=['reset', 'rs'],
        hidden=True,
        description="Reset suggestion counter to 1"
    )
    async def reset_suggestions(self, ctx):
        if (await self.bot.is_owner(ctx.author)):
            if (ctx.guild.id == 637316662801989658):
                decisionChannel = self.bot.get_channel(744413784319328286)
            else:
                decisionChannel = self.bot.get_channel(779541142818521108)

            await decisionChannel.purge()
            self.suggestionDB.clear()
            with open("suggestionID.txt", 'w') as f:
                f.write("1\n")
                await ctx.reply("Reset suggestions")


def setup(bot):
    bot.add_cog(GameNightCommands(bot))
