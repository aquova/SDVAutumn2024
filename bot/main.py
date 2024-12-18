# SDV Autumn 2024 Event Bot
# https://github.com/aquova/SDVAutumn2024
# 2024

import discord

from approval import post_entry
from client import client
from config import DISCORD_KEY, REDIRECT_CHANNELS

@client.event
async def on_ready():
    print('Logged in as')
    if client.user:
        print(client.user.name)
        print(client.user.id)
    await client.setup()

@client.event
async def on_guild_available(guild: discord.Guild):
    await client.sync_guild(guild)

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.channel.DMChannel):
        await message.channel.send("I am not the modmail bot.")
        return

    if message.channel.id in REDIRECT_CHANNELS:
        dest = REDIRECT_CHANNELS[message.channel.id]
        channel = client.get_channel(dest)
        if channel is not None:
            await post_entry(message, channel)

client.run(DISCORD_KEY)
