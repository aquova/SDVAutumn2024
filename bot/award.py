import discord

from utils import award_points

class AwardModal(discord.ui.Modal):
    def __init__(self, message: discord.Message):
        super().__init__(title="How many points to award?")
        self.message = message
        self.answer = discord.ui.TextInput(label="Must be a number")
        self.add_item(self.answer)

    async def on_submit(self, interaction: discord.Interaction):
        if self.message is None or self.message.guild is None:
            return
        try:
            delta = int(self.answer.value)
            await award_points(self.message.author, delta, self.message.guild.roles)
            await self.message.add_reaction("✅")
            await interaction.response.send_message(f"{delta} points awarded to {str(self.message.author)}", ephemeral=True)
        except ValueError:
            await interaction.response.send_message(f"{self.answer.value} isn't a number, try again", ephemeral=True)
