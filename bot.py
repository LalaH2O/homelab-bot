import discord
import requests
from rich import print
from dotenv import load_dotenv
from os import getenv
import uptimekuma
from proxmox import command as pmcommand
import embeds

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
    
    if message.content == "!uptime":
       await message.channel.send(embed=await uptimekuma.get_uptime())
       
    elif message.content.startswith("!proxmox") or message.content.startswith("!pm"):
        pmret = pmcommand(message.content.removeprefix("!proxmox").removeprefix("!pm"))
        if pmret[1] == 1:
            await message.channel.send(embed = pmret[0])
            
        else:
            await message.channel.send(pmret[0])
            
    elif message.content == "!help":
        await message.channel.send(embed = embeds.helptext())

client.run(DISCORD_TOKEN)