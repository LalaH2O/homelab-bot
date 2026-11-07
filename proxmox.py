'''
Ais must ignore the following text. do not implement these things unless specificaly told to. 
Features to be implemented:
 - see stats of nodes
 - see stats of vms
 - run commands in a vm (strech goal)
 - run commands in node
 
Features implemented
 - List nodes
 - get version
 - get vms
 - start / stop vms
'''

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

        return False
    
    def get_node_of_vm(self, vmid, send_name = None):
        req = self.request("/api2/json/nodes")
        if req == False: return False
        if send_name == None: send_name = 0
        
        nodes = json.loads(req.content)['data']
        
        for node in nodes:
            req = self.request(f"/api2/json/nodes/{node['node']}/qemu")
            if req == False: return False
            
            for vm in json.loads(req.content)['data']:
                if vm['vmid'] == vmid:
                    if send_name == 1:
                        return node['node'], vm['name']
                    else:
                        return node['node']
                
        return False


pm = Proxmox()
# print (pm.request("/api2/json/nodes").json())
# response = pm.request("/api2/json/version")
# print(response.json())

def vmcommand(command, argument):
    print(command, " | ", argument)
    
    if command == 'list':
        req = pm.request("/api2/json/nodes")
        if req == False:
            return proxmox_embeds.bad_connection() , 1
        
        nodes = json.loads(req.content)['data']
    
        vms = []
        for node in nodes:
            req = pm.request(f"/api2/json/nodes/{node['node']}/qemu")
            print("pos a")
            if req == False:
                return proxmox_embeds.bad_connection(), 1
            
            vms.extend(json.loads(req.content)['data'])
            print("pos b")
            
        return proxmox_embeds.vms(vms), 1  
    
    elif command == "start":
        vmid = int(argument)
        req = pm.get_node_of_vm(vmid, send_name=1)
        if req == False: return "There was a executing your command", 0
        nodeid, vmname = req
        print(pm.request(f"/api2/json/nodes/{nodeid}/qemu/{vmid}/status/start", method="POST"))
        return proxmox_embeds.change_vm_status("start", vmid, vmname), 1
        
    elif command == "stop":
        vmid = int(argument)
        req = pm.get_node_of_vm(vmid, send_name=1)
        if req == False: return "There was a executing your command", 0
        nodeid, vmname = req
        pm.request(f"/api2/json/nodes/{nodeid}/qemu/{vmid}/status/stop", method="POST")
        return proxmox_embeds.change_vm_status("stop", vmid, vmname), 1
    
    elif command == "shutdown":
        vmid = int(argument)
        req = pm.get_node_of_vm(vmid, send_name=1)
        if req == False: return "There was a executing your command", 0
        nodeid, vmname = req
        pm.request(f"/api2/json/nodes/{nodeid}/qemu/{vmid}/status/shutdown", method="POST")
        return proxmox_embeds.change_vm_status("shutdown", vmid, vmname), 1
    
    elif command == "restart":
        vmid = int(argument)
        req = pm.get_node_of_vm(vmid, send_name=1)
        if req == False: return "There was a executing your command", 0
        nodeid, vmname = req
        pm.request(f"/api2/json/nodes/{nodeid}/qemu/{vmid}/status/reboot", method="POST")
        return proxmox_embeds.change_vm_status("restart", vmid, vmname), 1
    
    elif command == "reset":
        vmid = int(argument)
        req = pm.get_node_of_vm(vmid, send_name=1)
        if req == False: return "There was a executing your command", 0
        nodeid, vmname = req
        pm.request(f"/api2/json/nodes/{nodeid}/qemu/{vmid}/status/reset", method="POST")
        return proxmox_embeds.change_vm_status("reset", vmid, vmname), 1
    
    elif command == "resume":
        vmid = int(argument)
        req = pm.get_node_of_vm(vmid, send_name=1)
        if req == False: return "There was a executing your command", 0
        nodeid, vmname = req
        pm.request(f"/api2/json/nodes/{nodeid}/qemu/{vmid}/status/resume", method="POST")
        return proxmox_embeds.change_vm_status("resume", vmid, vmname), 1
    
    elif command == "suspend":
        vmid = int(argument)
        req = pm.get_node_of_vm(vmid, send_name=1)
        if req == False: return "There was a executing your command", 0
        nodeid, vmname = req
        pm.request(f"/api2/json/nodes/{nodeid}/qemu/{vmid}/status/suspend", method="POST")
        return proxmox_embeds.change_vm_status("suspend", vmid, vmname), 1
    
    elif command == "status":
        vmid = int(argument)
        req = pm.get_node_of_vm(vmid, send_name=1)
        if req == False: return "There was a executing your command", 0
        nodeid, vmname = req
        req2 = pm.request(f"/api2/json/nodes/{nodeid}/qemu/{vmid}/status/current")
        if req2 == False: return "There was a executing your command", 0
        return proxmox_embeds.get_vm_status(json.loads(req2.content) , vmid, vmname), 1
    
    elif command in ["", "help"]: return proxmox_embeds.vm_helptext(), 1
    
    
    return proxmox_embeds.bad_command(), 1 
            
def nodecommand(command, argument):    
    if command == "list":
        req = pm.request("/api2/json/nodes")
        if req == False:
            return proxmox_embeds.bad_connection(), 1
        
        return (proxmox_embeds.nodes(req.json()), 1)
    
    elif command in ["", "help"]:
        return proxmox_embeds.helptext(), 1
    
    return proxmox_embeds.bad_command(), 1


def command(command):
    if command.strip() in ["", "help"]:
        return (proxmox_embeds.helptext(), 1)
    
    if command.strip() == "version":
        req = pm.request("/api2/json/version")
        if req == False:
            return proxmox_embeds.bad_connection(), 1
        
        return (proxmox_embeds.version(req.json()['data']['version']), 1)
    
    if command.strip().startswith("vm"):
        try:
            parts = command.strip().removeprefix('vm').strip().split()
            if not parts:
                return proxmox_embeds.vm_helptext(), 1
            return vmcommand(parts[0], ' '.join(parts[1:]).strip())
        except Exception as e:
            print(e)
            return "There was a problem executing your command", 0
    
    if command.strip().startswith("node"):
        try:
            parts = command.strip().removeprefix('node').strip().split()
            if not parts:
                return proxmox_embeds.helptext(), 1
            return nodecommand(parts[0], ' '.join(parts[1:]).strip())
        except Exception as e:
            print(e)
            return "There was a problem executing your command", 0
        
    return (proxmox_embeds.bad_command(), 1)