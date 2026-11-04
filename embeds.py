import discord
from random import choice

def helptext():
    generator = "https://embed.dan.onl/?data=eyJhdXRob3IiOnsibmFtZSI6IkhvbWVsYWIgYm90In0sInRpdGxlIjoiQ29tbWFuZHMiLCJmaWVsZHMiOlt7Im5hbWUiOiIhdXB0aW1lIiwidmFsdWUiOiJEaXNwbGF5IHRoZSB1cHRpbWUgb2YgYWxsIHVwdGltZWt1bWEgbW9uaXRvcnMuIn0seyJuYW1lIjoiIXByb3htb3giLCJ2YWx1ZSI6IkludGVyYWN0IHdpdGggdGhlIHByb3htb3ggYXBpLiBcbiFwcm94bW94IGZvciBtb3JlIGRldGFpbHMgb24gcHJveG1veCBzdWJjb21tYW5kcy4ifSx7Im5hbWUiOiIhaGVscCIsInZhbHVlIjoiRGlzcGxheSB0aGlzIGhlbHB0ZXh0LiJ9XSwiY29sb3IiOiIjMDAzMWY1In0%3D"
    embed = discord.Embed(title="Commands",
                          colour=0x0031f5)

    embed.set_author(name="Homelab bot")

    embed.add_field(name="!uptime",
                    value="Display the uptime of all uptimekuma monitors.",
                    inline=False)
    embed.add_field(name="!proxmox",
                    value="Interact with the proxmox api. \n!proxmox for more details on proxmox subcommands.",
                    inline=False)
    embed.add_field(name="!help",
                    value="Display this helptext.",
                    inline=False)
    
    return embed

class _uptimekuma_embeds():
    def __init__(self):
        pass
    
    def uptime(self, monitors, uptimes):
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

class _proxmox_embeds():
    def __init__(self): pass
        
    def helptext(self): 
        generator = "https://embed.dan.onl/?data=eyJhdXRob3IiOnsibmFtZSI6IkhvbWVsYWIgYm90In0sInRpdGxlIjoiUHJveG1veCBjb21tYW5kcyIsImZpZWxkcyI6W3sibmFtZSI6IiFwcm94bW94IHZlcnNpb24iLCJ2YWx1ZSI6IkRpc3BsYXkgdGhlIHByb3htb3ggdmVyc2lvbiJ9LHsibmFtZSI6IiFwcm94bW94IG5vZGVzIiwidmFsdWUiOiJEaXNwbGF5IGFsbCBwcm94bW94IG5vZGVzLiJ9LHsibmFtZSI6IiFwcm94bW94IiwidmFsdWUiOiJEaXNwbGF5IHRoaXMgaGVscHRleHQuIn1dLCJjb2xvciI6IiMwMDMxZjUifQ%3D%3D"
        embed = discord.Embed(title="Proxmox commands",
                          colour=0x0031f5)

        embed.set_author(name="Homelab bot")

        embed.add_field(name="!proxmox version",
                        value="Display the proxmox version",
                        inline=False)
        embed.add_field(name="!proxmox nodes",
                        value="Display all proxmox nodes.",
                        inline=False)
        embed.add_field(name="!proxmox",
                        value="Display this helptext.",
                        inline=False)

        return embed
    
    def bad_command(self):
        embed = discord.Embed(title=f"Bad proxmox command",
                              colour=0x8F1F00,
                              description="Try !proxmox help for help")
        
        embed.set_author(name="Homelab bot")
        
        return embed
        
    def version(self, version):
        embed = discord.Embed(title=f"Proxmox version {version}",
                              colour=0x1F4F00)
        
        embed.set_author(name="Homelab bot")
        
        return embed
    
    def nodes(self, data):
        embed = discord.Embed(title="Proxmox nodes")

        embed.set_author(name="Homelab bot")
        for node in data["data"]:
            if node['cpu'] < 0.3: emoji = "🟢"
            elif node['cpu'] < 0.8: emoji = "🟡"
            else: emoji = "🔴"
            
            embed.add_field(name=f"{node['node']}",
                            value=f'''{emoji} | CPU usage: {round(node['cpu']*100, 2)}%\n
                            {choice("🕛🕧🕐🕜🕑🕝")} | Uptime: {round(node['uptime']/60/60, 2)}h''',
                            inline=False)
            
        return embed
    
    def vms(self, data):
        embed = discord.Embed(title="Proxmox vms")

        embed.set_author(name="Homelab bot")
        for vm in data:
            if vm['status'] == "running": emoji = "🟢"
            else: emoji = "🔴"
            
            embed.add_field(name=f"{emoji} | {vm['name']} ({vm['vmid']})",
                            value = "",
                            inline=True)
            
        return embed
        
proxmox_embeds = _proxmox_embeds()
uptimekuma_embeds = _uptimekuma_embeds()