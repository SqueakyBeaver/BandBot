import discord
import os

from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.all()
token = os.environ.get("DISCORD_BOT_SECRET")


class BotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         command_prefix="b!",  # Change to desired prefix
                         case_insensitive=True,  # Commands aren't case-sensitive
                         intents=intents,  # Discord has to be annoying
                         owner_id=557273716782923820  # I own the bot
                         )
        extensions = [
            "cogs.devs",  # Commands for devs only
            # "cogs.game_night",  # Commands for game nights; I need to rewrite this
            "cogs.general",  # General commands
            "cogs.quotes",  # Quotes commands
            "cogs.moderation",  # Moderation commands
            "cogs.help",  # Help command
            "cogs.holidays",  # Holiday-related commands
            "cogs.starboard" # Starboard commands
        ]

        if __name__ == '__main__':  # Ensures this is the file being run
            for extension in extensions:
                self.load_extension(extension)  # Loads every extension.

    async def on_ready(self):  # When the bot is ready
        print("I'm in")
        print(self.user)  # Prints the bot's username and identifier


bot = BotClient()
keep_alive()  # Starts a webserver to be pinged.
bot.run(token)  # Starts the bot
