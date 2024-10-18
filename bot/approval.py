import discord
import requests

import db
from utils import award_points

FORWARD_URL = "https://catbox.moe/user/api.php"

class ApprovalButton(discord.ui.Button):
    def __init__(self, entry_user: discord.Member):
        self.entry_user = entry_user
        super().__init__(label="Approve", style=discord.ButtonStyle.primary)

    async def callback(self, interaction: discord.Interaction):
        if interaction.message is None or interaction.message.guild is None:
            return
        await interaction.response.send_modal(ApproveModal(self, self.entry_user))

class ApproveModal(discord.ui.Modal):
    def __init__(self, parent: ApprovalButton, user: discord.Member):
        super().__init__(title="How many points to award?")
        self.entry_user = user
        self.parent = parent
        self.answer = discord.ui.TextInput(label="Must be a number")
        self.add_item(self.answer)

    async def on_submit(self, interaction: discord.Interaction):
        if interaction.message is None or interaction.message.guild is None:
            return
        try:
            delta = int(self.answer.value)
            db.add_submission(interaction.message)
            await award_points(self.entry_user, delta, interaction.message.guild.roles)
            embed = interaction.message.embeds[0]
            self.parent.view.clear_items()
            self.parent.view.add_item(discord.ui.Button(label="Approved!", style=discord.ButtonStyle.green, disabled=True))
            await interaction.message.edit(embed=embed, view=self.parent.view)
            await interaction.response.defer()
        except ValueError:
            await interaction.response.send_message(f"{self.answer.value} isn't a number, try again", ephemeral=True)

class DenyButton(discord.ui.Button):
    def __init__(self, entry_user: discord.Member):
        self.entry_user = entry_user
        super().__init__(label="Deny", style=discord.ButtonStyle.red)

    async def callback(self, interaction: discord.Interaction):
        if interaction.message is None:
            return
        embed = interaction.message.embeds[0]
        self.view.clear_items()
        self.view.add_item(discord.ui.Button(label="Denied!", style=discord.ButtonStyle.red, disabled=True))
        await interaction.message.edit(embed=embed, view=self.view)
        await self.entry_user.send("We're sorry, but your submission been denied by the SDV staff. For additional info, please DM the Modmail bot.")
        await interaction.response.defer()

class EntryView(discord.ui.View):
    def __init__(self, entry_user: discord.Member):
        super().__init__(timeout=None)
        self.add_item(ApprovalButton(entry_user))
        self.add_item(DenyButton(entry_user))

async def post_entry(message: discord.Message, channel: discord.TextChannel):
    message_embed = discord.Embed(description=message.content, color=message.author.color)
    message_embed.add_field(name="Submitter:", value=message.author.mention)
    await channel.send(embed=message_embed, view=EntryView(message.author))

    for i, attachment in enumerate(message.attachments):
        embed = discord.Embed(description=f"Image submission {i + 1}", color=message.author.color)
        embed.add_field(name="Submitter:", value=message.author.mention)
        new_url = requests.post(FORWARD_URL, data={"reqtype": "urlupload", "url": attachment.url})
        if new_url.ok:
            embed.set_image(url=new_url.text)
        else:
            print(f"Something went wrong: {new_url.text}")
        await channel.send(embed=embed, view=EntryView(message.author))
    await message.delete()
