import discord
from discord.ext import commands

class SuggestionCommands(commands.Cog):
  """Suggestion Commands"""

  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='suggestgame', aliases=['sg'])
  async def suggest_game(self, ctx, *args):
    suggestionChannel = self.bot.get_channel(744413784319328286)
    await suggestionChannel.send(f'{0} suggested ```css{1}``` at `{2}`', ctx.author.mention, ' '.join(args), )

  @commands.command(name="test")
  async def test(self, ctx, *args):
      await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


def setup(bot):
  bot.add_cog(SuggestionCommands(bot))