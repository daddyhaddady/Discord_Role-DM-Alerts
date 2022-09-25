from os import getenv

from dotenv import load_dotenv

load_dotenv(".env")

from bot.bot import bot

if __name__ == "__main__":

    bot.run(getenv("TOKEN"))
