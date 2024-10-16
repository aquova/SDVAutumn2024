from enum import Enum, unique
from typing import Sequence

import discord

from config import EVENT_ROLES
import db

@unique
class Trick_Treat(Enum):
    TRICK = 1
    TREAT = 2

async def award_points(user: discord.Member, delta: int, available_roles: Sequence[discord.Role]):
    db.change_points(user, delta)
    # If they've received points, we'll consider them in the event and award the event roles
    for role_id in EVENT_ROLES:
        if not user.get_role(role_id):
            role = discord.utils.get(available_roles, id=role_id)
            if role is not None:
                await user.add_roles(role)

