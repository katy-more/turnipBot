import os
from discord.ext import commands
from dotenv import load_dotenv
import google_scripts

TOKEN = os.getenv('DISCORD_TOKEN')


def main():
    load_dotenv()

    # Initialize Google Sheets API connection
    sheet = google_scripts.api_setup()
    google_scripts.username_update(sheet=sheet)

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

        # When someone says turnipbot (case insensitive), turnipbot will
        # react to the message with the eyes emoji
        if "turnipbot" in message.content.lower():
            await message.add_reaction('👀')

        if str(message.channel) == os.getenv("STALK_CHANNEL"):
            content = message.content.split(" ")
            google_scripts.insert_by_username_date(
                sheet=sheet,
                username=message.author.name,
                date=message.created_at,
                value=content)
            await message.channel.send(str(message.created_at))

    bot.run(TOKEN)


if __name__ == '__main__':
    main()
