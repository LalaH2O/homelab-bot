import discord
import requests
from rich import print
from uptime_kuma_api import UptimeKumaApi # type: ignore
from dotenv import load_dotenv
from os import getenv

load_dotenv()

DISCORD_TOKEN = getenv("DISCORD_TOKEN")
KUMA_URL = getenv("KUMA_URL")
KUMA_NAME = getenv("KUMA_NAME")
KUMA_PWD = getenv("KUMA_PWD")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

api = UptimeKumaApi(KUMA_URL)
api.login(KUMA_NAME, KUMA_PWD)

def get_all_monitors():
    """
    Retrieve all monitors from an Uptime Kuma instance.

    Returns:
        list[dict]: Information about all configured monitors.
    """

    monitors = api.get_monitors()

    return monitors


# Example
monitors = get_all_monitors()

monitorids = []

for monitor in monitors:
    print(monitor)
    monitorids.append(monitor["id"])

async def get_uptime():
    uptimes = api.uptime()

    embed = discord.Embed(
        title="📊 Monitor Uptime",
        description="Uptime statistics over the last year",
        color=discord.Color.green()
    )

    for monitor in monitors:
        uptime = round(float(uptimes[monitor["id"]]["1y"]) * 100, 5)

        if uptime >= 99.9:
            status = "🟢"
        elif uptime >= 99:
            status = "🟡"
        else:
            status = "🔴"

        embed.add_field(
            name=f"{status} {monitor['name']}",
            value=f"`{uptime:.5f}".rstrip("0").rstrip(".") + "%`",
            inline=True
        )

    embed.set_footer(text="Uptime Kuma • Last 365 days")

    return embed

@client.event
async def on_ready():
    print(f'[green]We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == "uptime":
       await message.channel.send(embed=await get_uptime())

client.run(DISCORD_TOKEN)