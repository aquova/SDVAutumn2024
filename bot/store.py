import discord

from config import STORE
import db

class StoreItem(discord.SelectOption):
    def __init__(self, idx: int):
        item = STORE[idx]
        text = f"{item['name']} - {item['price']} points"
        emoji = None
        if item['emoji'] is not None:
            emoji = discord.PartialEmoji.from_str(item['emoji'])
        super().__init__(label=text, value=str(idx), emoji=emoji, default=False)

class StoreWidget(discord.ui.Select):
    def __init__(self):
        options: list[discord.SelectOption] = [StoreItem(i) for i in range(0, len(STORE))]
        super().__init__(custom_id="store_widget", options=options)

    async def callback(self, interaction: discord.Interaction):
        if isinstance(interaction.user, discord.User) or len(self.values) != 1:
            return
        idx = int(self.values[0])
        item = STORE[idx]
        player = db.get_player(interaction.user)
        if player.points < item['price']:
            await interaction.response.send_message(f"You only have {player.points} points, you can't afford this!", ephemeral=True)
            return
        if interaction.user.get_role(item['role']):
            await interaction.response.send_message("You have already purchased that role!", ephemeral=True)
            return
        role = discord.utils.get(interaction.user.guild.roles, id=item['role'])
        if role is None:
            raise AssertionError("Invalid role ID saved in config")
        await interaction.user.add_roles(role)
        db.change_points(interaction.user, -1 * item['price'])
        await interaction.response.send_message(f"You are now the proud owner of the {item['name']} role and have {player.points - item['price']} points remaining. Enjoy!", ephemeral=True)

class StoreView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(StoreWidget())
