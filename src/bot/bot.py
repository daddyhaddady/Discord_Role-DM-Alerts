from datetime import datetime
from sys import version as sys_version

import disnake
from disnake import __version__ as disnake_version
from disnake.ext import commands

from bot import __version__ as bot_version

# declare intents and instantiate the bot
intents = disnake.Intents.none()
intents.guilds = True
intents.members = True
intents.dm_messages = True

bot = commands.InteractionBot(reload=True, intents=intents)


@bot.listen()
async def on_ready():
    print(
        "----------------------------------------------------------------------\n"
        f'Bot started at: {datetime.now().strftime("%m/%d/%Y - %H:%M:%S")}\n'
        f"System Version: {sys_version}\n"
        f"Disnake Version: {disnake_version}\n"
        f"Bot Version: {bot_version}\n"
        f"Connected to Discord as {bot.user} ({bot.user.id})\n"
        f"Connected to {len(bot.guilds)} guilds with {len(bot.users)} members\n"
        "----------------------------------------------------------------------\n"
    )


bot.load_extensions("bot/cogs")
