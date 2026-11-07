from uptime_kuma_api import UptimeKumaApi # type: ignore
from dotenv import load_dotenv
from os import getenv
import discord
from embeds import uptimekuma_embeds
from webhook import print

load_dotenv()

KUMA_URL = getenv("KUMA_URL") or ""
KUMA_NAME = getenv("KUMA_NAME") or ""
KUMA_PWD = getenv("KUMA_PWD") or ""

# Initialize API with error handling
api = None
monitors = []
monitorids = []

def reauthenticate():
    """Attempt to reauthenticate with the Uptime Kuma API"""
    global api, monitors, monitorids
    try:
        api = UptimeKumaApi(KUMA_URL)
        api.login(KUMA_NAME, KUMA_PWD)
        
        def get_all_monitors():
            """
            Retrieve all monitors from an Uptime Kuma instance.

            Returns:
                list[dict]: Information about all configured monitors.
            """

            monitors = api.get_monitors() #type: ignore

            return monitors

        # Example
        monitors = get_all_monitors()

        monitorids = []

        for monitor in monitors:
            # print(monitor)
            monitorids.append(monitor["id"])
            
        return True
    except Exception as e:
        return False

# Initial authentication
try:
    api = UptimeKumaApi(KUMA_URL)
    api.login(KUMA_NAME, KUMA_PWD)
    
    def get_all_monitors():
        """
        Retrieve all monitors from an Uptime Kuma instance.

        Returns:
            list[dict]: Information about all configured monitors.
        """

        monitors = api.get_monitors() #type: ignore

        return monitors

    # Example
    monitors = get_all_monitors()

    monitorids = []

    for monitor in monitors:
        # print(monitor)
        monitorids.append(monitor["id"])
        
except Exception as e:
    # Check if we know we don't have access to the server
    # This could be determined by specific error types or messages
    if "unauthorized" in str(e).lower() or "forbidden" in str(e).lower():
        # We know we don't have access, don't retry
        pass  # Will be handled in get_uptime
    else:
        # Any other error, we'll handle it in get_uptime
        pass

async def get_uptime():
    try:
        uptimes = api.uptime() #type: ignore
        embed = uptimekuma_embeds.uptime(monitors, uptimes)
        return embed, 1
    except Exception as e:
        # Check if we know we don't have access to the server
        # This could be determined by specific error types or messages
        if "unauthorized" in str(e).lower() or "forbidden" in str(e).lower():
            # Try reauthentication once
            if reauthenticate():
                try:
                    uptimes = api.uptime() #type: ignore
                    embed = uptimekuma_embeds.uptime(monitors, uptimes)
                    return embed, 1
                except Exception as e2:
                    # Reauthentication succeeded but uptime still failed
                    return uptimekuma_embeds.bad_connection(), 1
            else:
                # We know we don't have access, don't retry
                return uptimekuma_embeds.bad_connection(), 1
        else:
            # Any other error, return bad connection
            return uptimekuma_embeds.bad_connection(), 1