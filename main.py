import discord
import os

from discord.ext import commands
from keep_alive import keep_alive

from datetime import datetime
from database import DBClient
from discord.ext import tasks


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


async def daily_ping():
    await bot.wait_until_ready()
    ping_channel = bot.get_channel(637316663267819561)
    while not bot.is_closed():
        pingUsers = reminderDB.dataset.find({})
        if (datetime.now().hour == 8 and datetime.now().minute == 0):
            pingStr = ""
            for userID in pingUsers:
                user = ping_channel.guild.get_member(userID["_id"])
                pingStr += f"{user.mention} "
            await ping_channel.send(f"{pingStr}\nYou are amazing, have a great day!")


keep_alive()  # Starts a webserver to be pinged.
bot.loop.create_task(daily_ping())
bot.run(token)  # Starts the bot
