from typing import cast

import discord
from discord.ext import commands

from config import TOT_CHANNEL
import db
from store import StoreView

class DiscordClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        # The command prefix is never used, but we have to have something
        super().__init__(command_prefix="$", intents=intents)
        db.initialize()

    async def setup(self):
        self.tot_log = cast(discord.TextChannel, self.get_channel(TOT_CHANNEL))

    async def sync_guild(self, guild: discord.Guild):
        import context
        self.add_view(StoreView())
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)

client = DiscordClient()
