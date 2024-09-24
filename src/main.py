# SDV Autumn 2024 Event Bot
# https://github.com/aquova/SDVAutumn2024
# 2024

import discord

from client import client
from config import DISCORD_KEY, REDIRECT_CHANNELS

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
                embed.set_image(url=message.attachments[0].url)
            await channel.send(embed=embed)
            await message.delete()

client.run(DISCORD_KEY)
