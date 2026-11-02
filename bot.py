import discord
import requests
from rich import print
from dotenv import load_dotenv
from os import getenv
import uptimekuma
import pong

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN") or ""

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"[green]We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author.bot:
        return

    command = message.content.strip().lower()

    if command == "uptime":
        await message.channel.send(embed=await uptimekuma.get_uptime())
    elif command in {"pong", "!pong"}:
        await pong.start_game(message.channel, message.author.id)


client.run(DISCORD_TOKEN)
