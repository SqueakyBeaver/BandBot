import discord
from discord.ext import commands
from database import DBClient


class Starboard(commands.Cog, name="starboard"):
    """Starboard related commands"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.starboard_info: DBClient = DBClient("starboard")
        self.guilds = self.starboard_info.find("guilds")

    def create_star_message(self, message: discord.Message, starred: list[discord.User]):
        e: discord.Embed = discord.Embed(colour=discord.Colour.random(),
                                         title="A new quality message by {0}#{1}"
                                         .format(message.author.display_name,
                                                 message.author.discriminator))

        e.set_thumbnail(url="https://i.redd.it/k9wl9ypumyp31.png")
        e.add_field(
            name="Message:\n", value=message.content if message.content else "No content")
        e.add_field(name="\nAuthor:\n", value=message.author.mention)
        e.add_field(name="\nSent in:\n",
                    value="**[#{0}]({1})**".format(message.channel.name, message.jump_url))

        if message.attachments:
            attachments = []
            attachment_urls = ""
            for i in message.attachments:
                attachments.append(i.url)
                if "image" in i.content_type:
                    e.set_image(url=i.url)
                for i in range(0, len(attachments)):
                    attachment_urls += "**[File {0}]({1})** ".format(
                        i + 1, attachments[i])
                e.add_field(name="\nAttachments:\n", value=attachment_urls)

        e.description = "Starred {0} times by {1}".format(
            len(starred), ', '.join([i.mention for i in starred]))

        return e

    @commands.command(name="starchannel")
    async def set_starboard_channel(self, ctx: commands.Context, channel: discord.TextChannel):
        self.guilds = self.starboard_info.find("guilds")
        self.guilds[str(ctx.guild.id)]["channel"] = channel.id
        self.starboard_info.update("guilds", self.guilds)

        await ctx.send("Starred messages will be sent to {0}".format(channel.mention))

    @commands.command(name="starthresh",
                      aliases=["staramount"]
                      )
    async def set_star_thresh(self, ctx: commands.Context, thresh: int):
        self.guilds = self.starboard_info.find("guilds")

        self.guilds[str(ctx.guild.id)]["thresh"] = thresh

        self.starboard_info.update("guilds", self.guilds)

        await ctx.send("The amount of stars needed to get a message to the starboard is now {0}".format(thresh))

    @ commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        self.guilds = self.starboard_info.find("guilds")
        guild_settings = self.guilds[str(payload.guild_id)]

        print(guild_settings)
        channel: discord.TextChannel = self.bot.get_channel(payload.channel_id)
        message: discord.Message = await channel.fetch_message(payload.message_id)

        for i in message.reactions:
            if i.emoji == "\U00002B50":
                starred = await i.users().flatten()

        if id := guild_settings["channel"]:
            star_channel = self.bot.get_channel(id)

        if thresh := guild_settings["thresh"]:
            star_thresh = thresh

        if len(message.reactions) == star_thresh:
            return await star_channel.send(embed=self.create_star_message(message, starred))

        if len(message.reactions) > star_thresh:
            return


def setup(bot: commands.Bot):
    bot.add_cog(Starboard(bot))
