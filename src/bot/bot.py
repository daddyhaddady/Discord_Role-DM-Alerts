"""
MIT License

Copyright (c) 2022 DLCHAMP

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
intents.messages = True

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
