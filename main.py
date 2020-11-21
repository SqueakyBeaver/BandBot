import os
from keep_alive import keep_alive
from discord.ext import commands
import discord

bot = commands.Bot(
    command_prefix="b!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
)

bot.author_id = 557273716782923820  # Change to your discord id!!!


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


extensions = [
    "cogs.devs",  # Commands for devs only
    "cogs.suggestions"  # Commands for everyone else
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loads every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("DISCORD_BOT_SECRET")
bot.run(token)  # Starts the bot
