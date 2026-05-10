import discord
import requests
import aiohttp
import asyncio

# --- CONFIG ---
TOKEN = 'MTExOTI3OTI2ODc2NjE2NzA2MQ.G71wCA.0-kDjddnnNWntFkHVk93vH37HcjSuh0Wf7lsxwMTExOTI3OTI2ODc2NjE2NzA2MQ.G71wCA.0-kDjddnnNWntFkHVk93vH37HcjSuh0Wf7lsxw'
BLOXLINK_KEY = 'd3ddb6f0-4992-454a-a0c4-57e97dc810a4'
PROXY = "http://proxy.server:3128" # The specific proxy for PythonAnywhere

class MyBot(discord.Client):
    async def setup_hook(self):
        # This tells the bot to use the PythonAnywhere proxy
        self.http.proxy = PROXY

    async def on_ready(self):
        print(f'Bot is online as {self.user}')

    async def on_guild_channel_create(self, channel):
        # Only trigger in ticket channels
        if "ticket-" not in channel.name:
            return
            
        await asyncio.sleep(3) # Wait for TicketsBot to set the topic
        
        # Grab Discord ID from the channel topic
        import re
        match = re.search(r'\d{17,19}', str(channel.topic))
        if not match: return
        
        discord_id = match.group()
        
        # Look up Bloxlink info
        url = f"https://api.blox.link/v4/public/guilds/{channel.guild.id}/discord-to-roblox/{discord_id}"
        headers = {"Authorization": BLOXLINK_KEY}
        
        # We use a standard request here since it's whitelisted
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "robloxID" in data:
                rid = data["robloxID"]
                # Send the Roblox card
                embed = discord.Embed(title="Roblox Linked Account", color=0x00ff00)
                embed.add_field(name="Roblox ID", value=rid)
                embed.add_field(name="Profile", value=f"[Click Here](https://www.roblox.com/users/{rid}/profile)")
                await channel.send(embed=embed)

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True

client = MyBot(intents=intents)
client.run(TOKEN)