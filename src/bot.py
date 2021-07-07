import discord
import os
import logging
import pytz

from datetime import datetime
from discord.ext import commands
from keep_alive import keep_alive

print(datetime.now(pytz.timezone("America/Chicago")))
intents = discord.Intents.all()
token = os.environ.get("DISCORD_BOT_SECRET")


class BotClient(commands.Bot):
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs,
                         command_prefix="b!",  # Change to desired prefix
                         case_insensitive=True,  # Commands aren't case-sensitive
                         intents=intents,  # Discord has to be annoying
                         owner_id=557273716782923820,  # I own the bot
                         activity=discord.Activity(type=discord.ActivityType.playing, name="A Kazoo") # He is playing a kazoo
                         )
        extensions = [
            "cogs.devs",  # Commands for devs only
            # "cogs.game_night",  # Commands for game nights; I need to rewrite this
            "cogs.general",  # General commands
            "cogs.quotes",  # Quotes commands
            "cogs.moderation",  # Moderation commands
            "cogs.help",  # Help command
            "cogs.holidays",  # Holiday-related commands
            "cogs.starboard", # Starboard commands
            "cogs.config", # Finally, some config
            "cogs.daily", # Took me long enough, eh?
            "cogs.misc", # Yes
            "cogs.error_handler", #handle them errors
        ]

        if __name__ == "__main__":  # Ensures this is the file being run
            for extension in extensions:
                self.load_extension(extension)  # Loads every extension.

    async def on_ready(self):  # When the bot is ready
        print("I'm in")
        print(self.user)  # Prints the bot's username and identifier

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='logs.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

bot = BotClient()
keep_alive()  # Starts a webserver to be pinged.
bot.run(token)  # Starts the bot
