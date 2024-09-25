# SDV Autumn 2024 Event Bot
# https://github.com/aquova/SDVAutumn2024
# 2024

import discord
import requests

from client import client
from config import DISCORD_KEY, REDIRECT_CHANNELS

FORWARD_URL = "https://0x0.st/"

@client.event
async def on_ready():
    print('Logged in as')
    if client.user:
        print(client.user.name)
        print(client.user.id)

@client.event
async def on_guild_available(guild: discord.Guild):
    await client.sync_guild(guild)

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.channel.id in REDIRECT_CHANNELS:
        dest = REDIRECT_CHANNELS[message.channel.id]
        channel = client.get_channel(dest)
        if channel is not None:
            embed = discord.Embed(title=str(message.author), description=message.content)
            if len(message.attachments) > 0:
                new_url = requests.post(FORWARD_URL, data={"url": message.attachments[0].url})
                if new_url.ok:
                    embed.set_image(url=new_url.text)
            await channel.send(embed=embed)
            await message.delete()

client.run(DISCORD_KEY)
