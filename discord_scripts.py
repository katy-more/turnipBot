import os
from discord.ext import commands
from dotenv import load_dotenv
import google_scripts

TOKEN = os.getenv('DISCORD_TOKEN')


def main():
    load_dotenv()

    # Initialize Google Sheets API connection
    sheet = google_scripts.api_setup()

    bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_ready():
        print(f'{bot.user} has connected to Discord!')
        for guild in bot.guilds:
            print(guild)

    @bot.event
    async def on_message(message):
        # check if the message was sent by the bot itself
        if message.author == bot.user:
            return

        if "turnipbot" in message.content.lower():
            await message.add_reaction('👀')

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
