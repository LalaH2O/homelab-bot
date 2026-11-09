import discord
import requests
from rich import print
from dotenv import load_dotenv
from os import getenv
import embeds
from webhook import print, tdebug, debug
import rich
from discord.ext import commands

from commands import (upimec, 
                      create_monitorc, 
                      proxmoxc, 
                      helpc, 
                      uptimekuma_available, 
                      proxmox_available)
    
load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN") or ""

intents = discord.Intents.default()
intents.message_content = True

description = '''
Bot to controll my homelab
'''

bot = commands.Bot(command_prefix='/', description=description, intents=intents)
    
@bot.event
async def on_ready():
    # Tell the type checker that User is filled up at this point
    assert bot.user is not None

    print(f'[green]Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.tree.sync()
    
@bot.tree.command(name="uptime")
async def uptime(interaction: discord.Interaction): await upimec(interaction.response.send_message)
    
@bot.tree.command(name="create_monitor")
async def create_monitor(interaction: discord.Interaction, name: str, url: str): await create_monitorc(interaction.response.send_message, name, url)
            
@bot.tree.command(name="proxmox")
async def proxmox(interaction: discord.Interaction, argument: str): await proxmoxc(interaction.response.send_message, argument)
            
@bot.tree.command(name="help")
async def help(interaction: discord.Interaction): await helpc(interaction.response.send_message)

@bot.event
async def on_message(message):
    
    rich.print(message)
    
    if message.author == bot.user: return

    if message.content == "!uptime": await upimec(message.channel.send)
    elif message.content.startswith("!proxmox") or message.content.startswith("!pm"): await proxmoxc(message.channel.send, message.content.removeprefix("!proxmox").removeprefix("!pm"))
    elif message.content == "!help": await helpc(message.channel.send)    
    
    if message.content == ".debug":
        msg = ""
        msg += f"{proxmox_available=}\n"
        msg += f"{uptimekuma_available=}\n"
        msg += f"{message=}\n"
        msg += f"{debug=}\n"
        await message.channel.send(msg)
        
    elif message.content == ".debug toggle":
        tdebug()
        await message.channel.send(f"Toggled debug to {debug}")

if __name__ == '__main__': bot.run(DISCORD_TOKEN)