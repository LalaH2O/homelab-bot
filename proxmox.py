from rich import print
from dotenv import load_dotenv
from os import getenv
import discord
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

load_dotenv()

PROXMOX_TOKEN = getenv("PROXMOX_TOKEN") or ""
PROXMOX_URL0 = getenv("PROXMOX_URL0") or ""
PROXMOX_URL1 = getenv("PROXMOX_URL1") or ""
PROXMOX_URL2 = getenv("PROXMOX_URL2") or ""
PROXMOX_TOKEN_ID = getenv("PROXMOX_TOKEN_ID") or ""

class proxmox:
    def __init__(self):
        self.headers = {
            "Authorization": f"PVEAPIToken={PROXMOX_TOKEN_ID}={PROXMOX_TOKEN}"
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def request(self, endpoint, method = "GET"):
        SERVERS = [PROXMOX_URL0, PROXMOX_URL1, PROXMOX_URL2]
        for server in SERVERS:
            try:
                response = requests.request(
                    method,
                    f"{server}{endpoint}",
                    timeout=3,
                    verify=True
                )

                response.raise_for_status()
                return response

            except requests.RequestException as e:
                print(f"Server {server} failed: {e}")

        raise ConnectionError("All servers are unavailable")