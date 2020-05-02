import os
import discord
from dotenv import load_dotenv
import google_scripts

TOKEN = os.getenv('DISCORD_TOKEN')


def main():
    load_dotenv()

    # Initialize Google Sheets API connection
    sheet = google_scripts.api_setup()

    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'{client.user} has connected to Discord!')

    @client.event
    async def on_member_join(member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Hi {member.name}, welcome!'
        )

    client.run(TOKEN)


if __name__ == '__main__':
    main()