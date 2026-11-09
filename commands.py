from rich import print
import embeds
from webhook import print, tdebug, debug
import rich
from discord.ext import commands

try:
    import uptimekuma
    uptimekuma_available = 1
    
except Exception as e:
    uptimekuma = None
    print(f"[red]Uptimekuma unavailable \n {e}")
    uptimekuma_available = 0
    
try:
    from proxmox import command as pmcommand
    proxmox_available = 1
    
except Exception as e:
    pmcommand = None
    print(f"[red]Proxmox unavailable \n {e}")
    proxmox_available = 0

async def upimec(func):
    if uptimekuma_available == 1:
        assert uptimekuma is not None
        ukret = await uptimekuma.get_uptime()
        if ukret[1] == 1:
            func(embed = ukret[0])
        else: 
            func(ukret[0])
    else:
        func(embed = embeds.command_unavailable())

async def create_monitorc(func, name, url):
    assert uptimekuma is not None
    if uptimekuma_available == 1:
        func(embed = uptimekuma.create_monitor(name, url))
    else:
        func(embed = embeds.command_unavailable())

async def proxmoxc(func, argument):
    if proxmox_available == 1:
        assert pmcommand is not None
        pmret = pmcommand(argument)
        if pmret[1] == 1:
            func(embed = pmret[0])
        else:
            func(pmret[0])
    else:
        func(embed = embeds.command_unavailable())
        
async def helpc(func):
    func(embed=embeds.helptext())