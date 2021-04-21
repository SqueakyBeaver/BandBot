from discord.ext import commands
from database import DBClient
import discord


class Commands(commands.Cog, name="config"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.starboard_info: DBClient = DBClient("starboard")
        self.daily_info: DBClient = DBClient("daily")
        self.starboard_guilds: dict = self.starboard_info.find("guilds")
        self.daily_guilds: dict = self.daily_info.find("guilds")

    def check_if_exist(self, guild: discord.Guild):
        if not str(guild.id) in self.starboard_guilds.keys():
            self.starboard_guilds[str(guild.id)] = {
                "channel": 0, "sent": False, "role": 0, "tz": ""}
            self.starboard_info.update("guilds", self.starboard_guilds)

        if not str(guild.id) in self.daily_guilds.keys():
            self.daily_guilds[str(guild.id)] = {
                "channel": 0, "sent": False, "role": 0, "tz": ""}
            self.daily_info.update("guilds", self.daily_guilds)

    @commands.group(name="config",
                    aliases=["configure"])
    async def config(self, ctx: commands.Context):
        self.check_if_exist(ctx.guild)

        if ctx.invoked_subcommand == None:
            await ctx.reply("Invalid option\nThe options are `b!config daily` or `b!config starboard`")

    @config.group(name="starboard")
    async def starboard(self, ctx: commands.Context):
        """Configure the Starboard"""

        if ctx.invoked_subcommand == None:
            await ctx.reply("Options: `channel`, `thresh`")

    @starboard.command(name="channel")
    async def set_starboard_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """The channel where starred messages are sent"""
        self.check_if_exist(ctx.guild)

        self.starboard_guilds = self.starboard_info.find("guilds")
        try:
            self.starboard_guilds[str(ctx.guild.id)]["channel"] = channel.id
        except:
            self.starboard_guilds[str(ctx.guild.id)] = {}
            self.starboard_guilds[str(ctx.guild.id)]["channel"] = channel.id
        self.starboard_info.update("guilds", self.starboard_guilds)

        await ctx.reply("Starred messages will be sent to {0}".format(channel.mention))

    @starboard.command(name="thresh",
                       aliases=["amount"]
                       )
    async def set_star_thresh(self, ctx: commands.Context, thresh: int):
        """The amount of stars needed for a message to get sent to the starboard"""
        self.check_if_exist(ctx.guild)

        self.starboard_guilds = self.starboard_info.find("guilds")

        self.starboard_guilds[str(ctx.guild.id)]["thresh"] = thresh

        self.starboard_info.update("guilds", self.starboard_guilds)

        await ctx.reply("The amount of stars needed to get a message to the starboard is now {0}".format(thresh))

    @config.group(name="daily")
    async def daily(self, ctx: commands.Context):
        """Configure the daily post"""
        self.check_if_exist(ctx.guild)

        if ctx.invoked_subcommand == None:
            await ctx.reply("Options: `channel`, `timezone`, `ping`")

    @daily.command(name="channel")
    async def _daily_channel(self, ctx: commands.Context, channel: discord.TextChannel = None):
        """Set where the daily post will be sent"""
        self.check_if_exist(ctx.guild)

        self.daily_guilds[str(ctx.guild.id)]["channel"] = channel.id
        self.daily_info.update("guilds", self.daily_guilds)
        await ctx.reply("New daily post channel is {0}".format(channel.mention))

    @daily.command(name="timezone",
                   aliases=["tz"])
    async def _timezone(self, ctx: commands.Context, tz: str = None):
        """Set the timezone for the guild"""
        self.check_if_exist(ctx.guild)

        self.daily_guilds[str(ctx.guild.id)]["tz"] = tz
        self.daily_info.update("guilds", self.daily_guilds)
        await ctx.reply("New daily timezone is {0}".format(tz))

    @daily.command(name="ping",
                   aliases=["role"])
    async def _daily_ping_role(self, ctx: commands.Context, role: discord.Role = None):
        """Set the role to be pinged during the daily post"""
        self.check_if_exist(ctx.guild)

        self.daily_guilds[str(ctx.guild.id)]["role"] = role.id
        self.daily_info.update("guilds", self.daily_guilds)
        await ctx.reply("New daily ping role is {0}".format(role.mention))


def setup(bot: commands.Bot):
    bot.add_cog(Commands(bot))

# if ctx.invoked_subcommand == None:
