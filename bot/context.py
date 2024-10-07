import discord

from approval import award_points
from client import client
from config import LEADERBOARD_URL
import db
from store import StoreView
from utils import Trick_Treat

@client.tree.command(name="addpoints", description="Add/Remove points from users")
@discord.app_commands.describe(user="User", delta="Points to add/remove")
async def addpoints_slash(interaction: discord.Interaction, user: discord.Member, delta: int):
    await award_points(user, delta, interaction.user.guild.roles)
    await interaction.response.send_message(f"{delta} points have been given to {str(user)}", ephemeral=True)

@client.tree.command(name="leaderboard", description="Post the leaderboard for the event")
async def leaderboard_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"The event leaderboard can be viewed here: {LEADERBOARD_URL}")

@client.tree.command(name="points", description="Show how many points you have")
async def points_slash(interaction: discord.Interaction):
    player = db.get_player(interaction.user)
    await interaction.response.send_message(f"You have {player.points} points!", ephemeral=True)

@client.tree.command(name="poststore", description="Post the event store")
@discord.app_commands.describe(channel="Channel to post in")
async def poststore_slash(interaction: discord.Interaction, channel: discord.TextChannel):
    await channel.send("Step right up to the Event Store!\nSelect an item to purchase it!", view=StoreView())
    await interaction.response.send_message("Store posted!")

@client.tree.command(name="stats", description="Get info about your Event stats")
async def stats_slash(interaction: discord.Interaction):
    player = db.get_player(interaction.user)
    embed = discord.Embed(title=str(interaction.user), type="rich", color=interaction.user.color)
    embed.add_field(name="Points", value=player.points, inline=False)
    embed.add_field(name="Tricks Sent", value=player.tricks_sent)
    embed.add_field(name="Tricks Received", value=player.tricks_received)
    embed.add_field(name="Tricks Remaining", value=player.tricks_remaining)
    embed.add_field(name="Treats Sent", value=player.treats_sent)
    embed.add_field(name="Treats Received", value=player.treats_received)
    embed.add_field(name="Treats Remaining", value=player.treats_remaining)
    await interaction.response.send_message(embed=embed)

@client.tree.context_menu(name="Send Trick")
async def trick_message_context(interaction: discord.Interaction, message: discord.Message):
    if not message.author.bot:
        response = trick_treat_helper(interaction, message.author, Trick_Treat.TRICK)
        await message.add_reaction("🦇")
        await interaction.response.send_message(response, ephemeral=True)

@client.tree.context_menu(name="Send Trick")
async def trick_user_context(interaction: discord.Interaction, user: discord.Member):
    if not user.bot:
        response = trick_treat_helper(interaction, user, Trick_Treat.TRICK)
        await interaction.response.send_message(response, ephemeral=True)

@client.tree.context_menu(name="Send Treat")
async def treat_message_context(interaction: discord.Interaction, message: discord.Message):
    if not message.author.bot:
        response = trick_treat_helper(interaction, message.author, Trick_Treat.TREAT)
        await message.add_reaction("🍬")
        await interaction.response.send_message(response, ephemeral=True)

@client.tree.context_menu(name="Send Treat")
async def treat_user_context(interaction: discord.Interaction, user: discord.Member):
    if not user.bot:
        response = trick_treat_helper(interaction, user, Trick_Treat.TREAT)
        await interaction.response.send_message(response, ephemeral=True)

def trick_treat_helper(interaction: discord.Interaction, target: discord.User | discord.Member, tot: Trick_Treat) -> str:
    word = "treat" if tot == Trick_Treat.TREAT else "trick"
    if interaction.user == target:
        return f"You can't send a {word} to yourself..."
    if not db.has_tot(interaction.user, tot):
        return f"You don't have any remaining {word}s to give!"
    db.use_tot(interaction.user, target, tot)
    return f"You sent {str(target)} a {word}!"
