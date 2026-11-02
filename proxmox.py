
from rich import print
from dotenv import load_dotenv
from os import getenv
import requests

load_dotenv()

PROXMOX_TOKEN = getenv("PROXMOX_TOKEN") or ""
PROXMOX_URL0 = getenv("PROXMOX_URL0") or ""
PROXMOX_URL1 = getenv("PROXMOX_URL1") or ""
PROXMOX_URL2 = getenv("PROXMOX_URL2") or ""
PROXMOX_TOKEN_ID = getenv("PROXMOX_TOKEN_ID") or ""


class Proxmox:
    def __init__(self):
        self.headers = {
            "Authorization": f"PVEAPIToken={PROXMOX_TOKEN_ID}={PROXMOX_TOKEN}"
        }

        self.session = requests.Session()
        self.session.headers.update(self.headers)

        self.servers = [
            PROXMOX_URL0,
            PROXMOX_URL1,
            PROXMOX_URL2
        ]

    def request(self, endpoint, method="GET", **kwargs):
        for server in self.servers:
            if not server:
                continue

            try:
                response = self.session.request(
                    method,
                    f"{server.rstrip('/')}/{endpoint.lstrip('/')}",
                    timeout=5,
                    verify=False,
                    **kwargs
                )

                response.raise_for_status()
                return response

            except requests.RequestException as e:
                print(f"[red]Server {server} failed: {e}[/red]")

        raise ConnectionError("All Proxmox servers are unavailable")


pm = Proxmox()

response = pm.request("/api2/json/version")
print(response.json())