import discord
import requests
from rich import print
from dotenv import load_dotenv
from os import getenv
import embeds

try:
    import uptimekuma
    uptimekuma_available = 1
    
except Exception as e:
    print(f"[red]Uptimekuma unavailable \n {e}")
    uptimekuma_available = 0
    
try:
    from proxmox import command as pmcommand
    proxmox_available = 1
    
except Exception as e:
    print(f"[red]Proxmox unavailable \n {e}")
    proxmox_available = 0
    
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
    
    print(message)
    
    if message.author == client.user:
        return
    
    if message.content == "!uptime":
        ukret = await uptimekuma.get_uptime() #type: ignore
        if ukret[1] == 1: #type: ignore
            if uptimekuma_available == 1:
                await message.channel.send(embed=ukret[0]) #type: ignore
            else: 
                message.channel.send(embed = embeds.command_unavailable())
        else:
            await message.channel.send(ukret[0]) #type: ignore
       
    elif message.content.startswith("!proxmox") or message.content.startswith("!pm"):
        if proxmox_available == 1:
            pmret = pmcommand(message.content.removeprefix("!proxmox").removeprefix("!pm")) #type: ignore
            if pmret[1] == 1:
                await message.channel.send(embed = pmret[0])

            else:
                await message.channel.send(pmret[0])
        else:
            await message.channel.send(embed = embeds.command_unavailable())
            
    elif message.content == "!help":
        await message.channel.send(embed = embeds.helptext())

if __name__ == '__main__': client.run(DISCORD_TOKEN)