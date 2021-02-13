# bot.py
import os

import discord
from discord import utils as dutils
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

game = "_x________🐈\n nextrow"


@client.event
async def on_ready():
    guild = dutils.get(client.guilds, name=GUILD)
    textchannel = dutils.get(guild.channels, name="allmänt")
    await textchannel.send(
        f'{client.user} has connected to guild: {guild.name}(id:{guild.id})\n')
    members = "\n - ".join([member.name for member in guild.members])
    print(f'Members of the guild:\n {members}')


@client.event
async def on_member_join(member):
    print(f'member {member} joined. tring to send dm')
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, I am a dumb robot'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("!play"):
        await message.channel.send(game)


client.run(TOKEN)
