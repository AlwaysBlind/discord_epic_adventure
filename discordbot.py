# bot.py
import os

import discord
import asyncio
from discord import utils as dutils
from dotenv import load_dotenv
from game import Game

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

game = Game()


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
    if game.active:
        if message.content.startswith("hide"):
            game.hide()
        elif message.content.startswith("run"):
            game.run()
        elif (message.content.startswith("gun") or
              message.content.startswith("brutal vio")):
            game.gun()
        elif (message.content.startswith("feed")):
            game.feed()
        await message.delete()
    elif message.content.startswith("!play"):
        game.start()
        game_message = await message.channel.send(game.draw())
        while game.active:
            await asyncio.sleep(0.4)
            game.update()
            await game_message.edit(content=game.draw())


client.run(TOKEN)
