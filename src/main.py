# SDV Autumn 2024 Event Bot
# https://github.com/aquova/SDVAutumn2024
# 2024

import discord

import config
from client import client

"""
On Ready

Occurs when Discord bot is first brought online
"""
@client.event
async def on_ready():
    print('Logged in as')
    if client.user:
        print(client.user.name)
        print(client.user.id)

"""
On Guild Available

Runs when a guild (server) becomes available to the bot
"""
@client.event
async def on_guild_available(guild: discord.Guild):
    await client.sync_guild(guild)

client.run(config.DISCORD_KEY)
