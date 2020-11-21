import discord
from discord.ext import commands


class SuggestionCommands(commands.Cog):
    """Suggestion Commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='suggestgame', aliases=['sg'])
    async def suggest_game(self, ctx, *args):
        suggestionChannel = self.bot.get_channel(744413784319328286)
        suggestion_author = f'{ctx.author.name}#{ctx.author.discriminator}'

        await suggestionChannel.send(
            'At `{}`, **{}** suggested:```css\n{}``` '.format(ctx.message.created_at,
                                                               suggestion_author, ' '.join(args)))

    @commands.command(name="choose")
    async def choose_game(self, ctx, id):
        acceptRole = ctx.guild.get_role(732078243875651677)
        if (acceptRole in ctx.author.roles):
            try:
                accepted = await ctx.fetch_message(id)
                acceptedMessage = accepted.content
            except:
                await ctx.send("Invalid message id")
                return

            announcementChannel = self.bot.get_channel(637316663267819561)
            await announcementChannel.send(f'We will play {acceptedMessage[acceptedMessage.find("```css"):]} {ctx.guild.default_role}')


def setup(bot):
    bot.add_cog(SuggestionCommands(bot))
