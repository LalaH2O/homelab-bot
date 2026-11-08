import discord
import requests
from rich import print
from dotenv import load_dotenv
from os import getenv
import embeds
from webhook import print, tdebug, debug
import rich
from discord.ext import commands

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

description = '''
Bot to controll my homelab
'''

bot = commands.Bot(command_prefix='/', description=description, intents=intents)

@bot.event
async def on_ready():
    # Tell the type checker that User is filled up at this point
    assert bot.user is not None

    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    await bot.tree.sync(guild=discord.Object(id=1558574978314535094))
    
@bot.tree.command(name="uptime")
async def uptime(interaction: discord.Interaction):
        ukret = await uptimekuma.get_uptime() #type: ignore
        if ukret[1] == 1: #type: ignore
            if uptimekuma_available == 1:
                await interaction.response.send_message(embed=ukret[0]) #type: ignore
            else: 
                await interaction.response.send_message(embed = embeds.command_unavailable())
        else:
            await interaction.response.send_message(ukret[0]) #type: ignore
    
@bot.tree.command(name="create_monitor")
async def create_monitor(interaction: discord.Interaction, name: str, url: str):
    if uptimekuma_available == 1:
        await interaction.response.send_message(embed = uptimekuma.create_monitor(name, url)) #type: ignore
    else:
        await interaction.response.send_message(embed = embeds.command_unavailable())
            
@bot.tree.command(name="proxmox")
async def proxmox(interaction: discord.Interaction, argument: str):
        if proxmox_available == 1:
            pmret = pmcommand(argument) #type: ignore
            if pmret[1] == 1:
                await interaction.response.send_message(embed = pmret[0])

            else:
                await interaction.response.send_message(pmret[0])
        else:
            await interaction.response.send_message(embed = embeds.command_unavailable())
            
@bot.tree.command(name="help")
async def help(interaction: discord.Interaction):
    await interaction.response.send_message(embed=embeds.helptext())

@bot.event
async def on_message(message):
    
    rich.print(message)
    
    if message.author == bot.user:
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