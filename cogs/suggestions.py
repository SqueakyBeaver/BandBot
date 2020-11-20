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
            '**{}** suggested: ```css\n{}``` at `{}`'.format(
                suggestion_author, ' '.join(args), ctx.message.created_at))

    @commands.command(name="test")
    async def test(self, ctx, *args):
        await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


def setup(bot):
    bot.add_cog(SuggestionCommands(bot))
