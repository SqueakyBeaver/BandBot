import discord
import os
import cogs.daily_reminder as daily_reminder

from discord.ext import commands
from keep_alive import keep_alive
from database import DBClient

reminderDB = DBClient("dailyReminder")
intents = discord.Intents.all()
token = os.environ.get("DISCORD_BOT_SECRET")

bot = commands.Bot(
    command_prefix="b!",  # Change to desired prefix
    case_insensitive=True,  # Commands aren't case-sensitive
    intents=intents,  # Discord has to be annoying
    owner_id=557273716782923820  # I own the bot
)


@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier


extensions = [
    "cogs.devs",  # Commands for devs only
    "cogs.game_night",  # Commands for game nights
    "cogs.general",  # General commands
    "cogs.daily_reminder"  # Daily reminder pings
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loads every extension.


keep_alive()  # Starts a webserver to be pinged.
bot.loop.create_task(daily_reminder.daily_ping(bot))
bot.run(token)  # Starts the bot
