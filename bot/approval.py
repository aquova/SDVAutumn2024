import discord
import requests
from typing import Sequence

from config import EVENT_ROLES
import db

FORWARD_URL = "https://catbox.moe/user/api.php"
APPROVAL_POINTS = 10 # Make config param?

class ApprovalButton(discord.ui.Button):
    def __init__(self, entry_user: discord.Member):
        self.entry_user = entry_user
        super().__init__(label="Approve", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        if interaction.message is None or interaction.message.guild is None:
            return
        await award_points(self.entry_user, APPROVAL_POINTS, interaction.message.guild.roles)
        embed = interaction.message.embeds[0]
        self.view.remove_item(self)
        self.view.add_item(ApprovedButton())
        await interaction.message.edit(embed=embed, view=self.view)
        await interaction.response.defer()

class ApprovedButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Approved!", style=discord.ButtonStyle.success)

    # Need a dummy button so the interaction won't hang
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

class EntryView(discord.ui.View):
    def __init__(self, entry_user: discord.Member):
        super().__init__(timeout=None)
        self.entry_user = entry_user
        self.add_item(ApprovalButton(entry_user))

async def award_points(user: discord.Member, delta: int, available_roles: Sequence[discord.Role]):
    db.change_points(user, delta)
    # If they've received points, we'll consider them in the event and award the event roles
    for role_id in EVENT_ROLES:
        if not user.get_role(role_id):
            role = discord.utils.get(available_roles, id=role_id)
            if role is not None:
                await user.add_roles(role)

async def post_entry(message: discord.Message, channel: discord.TextChannel):
    embed = discord.Embed(title=str(message.author), description=message.content, color=message.author.color)
    if len(message.attachments) > 0:
        new_url = requests.post(FORWARD_URL, data={"reqtype": "urlupload", "url": message.attachments[0].url})
        if new_url.ok:
            embed.set_image(url=new_url.text)
        else:
            print(f"Something went wrong: {new_url.text}")
    await channel.send(embed=embed, view=EntryView(message.author))
    await message.delete()
