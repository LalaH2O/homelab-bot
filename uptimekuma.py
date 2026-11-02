from rich import print
from uptime_kuma_api import UptimeKumaApi # type: ignore
from dotenv import load_dotenv
from os import getenv
import discord
from embeds import uptimekuma_embeds

load_dotenv()

KUMA_URL = getenv("KUMA_URL") or ""
KUMA_NAME = getenv("KUMA_NAME") or ""
KUMA_PWD = getenv("KUMA_PWD") or ""

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
    # print(monitor)
    monitorids.append(monitor["id"])

async def get_uptime():
    uptimes = api.uptime()

    embed = uptimekuma_embeds.uptime(monitors, uptimes)

    return embed