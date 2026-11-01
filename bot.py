import discord
import requests
from rich import print
from dotenv import load_dotenv
from os import getenv
import uptimekuma

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN") or ""

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'[green]We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == "uptime":
       await message.channel.send(embed=await uptimekuma.get_uptime())

client.run(DISCORD_TOKEN)