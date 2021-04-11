import discord
from discord.ext import commands
from database import DBClient


class Starboard(commands.Cog, name="starboard"):
    """Starboard related commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.starboard_info: DBClient = DBClient("starboard info")

    @commands.command(name="starboard set channel",
                      aliases=["set starboard channel"])
    async def set_starboard_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        self.starboard_info.update({"guild": ctx.guild.id}, {
                                   "$set": {"channel": channel.id}})

        await ctx.send("Starred messages will be sent to {0}".format(channel.mention))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        try:
            guild_settings = self.starboard_info.find(
                {"guild": payload.guild_id})
        except:
            guild_settings = self.starboard_info.add(
                {"guild": payload.guild_id})
        print(guild_settings)
        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)
        message: discord.Message = await channel.fetch_message(payload.message_id)

        if id := guild_settings["channel"]:
            star_channel = self.bot.get_channel(id)

        if thresh := guild_settings["thresh"]:
            star_thresh = thresh

        if len(message.reactions) >= star_thresh:
            pass


def setup(bot: commands.Bot):
    bot.add_cog(Starboard(bot))
