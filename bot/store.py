from ast import literal_eval

import discord

from config import STORE
import db

class EmojiItem(discord.SelectOption):
    def __init__(self, idx: int):
        item = STORE[idx]
        text = f"{item['name']} - {item['price']} points"
        emoji = None
        value = {"type": "emoji", "idx": idx}
        if item['emoji'] is not None:
            emoji = discord.PartialEmoji.from_str(item['emoji'])
        super().__init__(label=text, value=str(value), emoji=emoji, default=False)

class TotItem(discord.SelectOption):
    def __init__(self, cost: int, receive: int):
        text = f"{receive} Tricks/Treats - {cost} points"
        value = {"type": "tot", "cost": cost, "receive": receive}
        super().__init__(label=text, value=str(value), default=False)

class StoreWidget(discord.ui.Select):
    def __init__(self):
        options: list[discord.SelectOption] = [EmojiItem(i) for i in range(0, len(STORE))]
        options.append(TotItem(cost=10, receive=5))
        super().__init__(custom_id="store_widget", options=options)

    async def callback(self, interaction: discord.Interaction):
        if len(self.values) != 1:
            return
        info = literal_eval(self.values[0])
        match info["type"]:
            case "emoji":
                await grant_emoji(interaction, info["idx"])
            case "tot":
                await grant_tot(interaction, info["cost"], info["receive"])
            case _:
                print("Unknown SelectOption type")
        # TODO: Need to somehow return selection to the placeholder

class StoreView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(StoreWidget())

async def grant_emoji(interaction: discord.Interaction, idx: int):
    if isinstance(interaction.user, discord.User):
        return
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

async def grant_tot(interaction: discord.Interaction, cost: int, receive: int):
    if isinstance(interaction.user, discord.User):
        return
    player = db.get_player(interaction.user)
    if player.points < cost:
        await interaction.response.send_message(f"You only have {player.points} points, you can't afford this!", ephemeral=True)
        return
    db.change_points(interaction.user, -1 * cost)
    db.grant_tot(interaction.user, receive)
    await interaction.response.send_message(f"You have received {receive} more tricks and treats, use them wisely!", ephemeral=True)

