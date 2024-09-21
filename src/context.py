import discord

from client import client
import db
from store import StoreView

@client.tree.command(name="addpoints", description="Add/Remove points from users")
@discord.app_commands.describe(user="User", delta="Points to add/remove")
async def addpoints_slash(interaction: discord.Interaction, user: discord.Member, delta: int):
    db.change_points(user.id, delta)
    await interaction.response.send_message(f"{delta} points have been given to {str(user)}", ephemeral=True)

@client.tree.command(name="points", description="Show how many points you have")
async def points_slash(interaction: discord.Interaction):
    player = db.get_player(interaction.user.id)
    await interaction.response.send_message(f"You have {player.points} points!", ephemeral=True)

@client.tree.command(name="poststore", description="Post the event store")
@discord.app_commands.describe(channel="Channel to post in")
async def poststore_slash(interaction: discord.Interaction, channel: discord.TextChannel):
    await channel.send("Step right up to the Event Store!\nSelect an item to purchase it!", view=StoreView())
    await interaction.response.send_message("Store posted!")
