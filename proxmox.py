
from rich import print
from dotenv import load_dotenv
from os import getenv
import requests
from embeds import proxmox_embeds
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
# print (pm.request("/api2/json/nodes").json())
# response = pm.request("/api2/json/version")
# print(response.json())

def vmcommand(command):
    if command in ['list', '']:
        nodes = json.loads(pm.request("/api2/json/nodes").content)
    
        vms = []
        
        for node in nodes:
            vms.extend(json.loads(pm.request(f"/api2/json/nodes/{node['id']}/qemu").content)['data'])
            
        return proxmox_embeds.vms(vms), 1  
    
    return proxmox_embeds.bad_command(), 1 
            
def command(command):
    if command.strip() in ["", "help"]:
        return (proxmox_embeds.helptext(), 1)
    
    if command.strip() == "version":
        return (proxmox_embeds.version(pm.request("/api2/json/version").json()['data']['version']), 1)
    
    if command.strip() == "nodes":
        return (proxmox_embeds.nodes(pm.request("/api2/json/nodes").json()), 1)
    
    if command.strip() == "vm":
        return vmcommand(command.strip().removeprefix('vm').strip())
    
    return (proxmox_embeds.bad_command(), 1)