from dataclasses import dataclass
import sqlite3

import discord

from config import DATABASE_PATH
from utils import Trick_Treat

@dataclass
class Player:
    points: int
    tricks_remaining: int
    treats_remaining: int
    tricks_sent: int
    treats_sent: int
    tricks_received: int
    treats_received: int


def initialize():
    sqlconn = sqlite3.connect(DATABASE_PATH)
    # TODO: Figure out how to pass in the default values here
    CREATION_QUERY = """
    CREATE TABLE IF NOT EXISTS players (\
    uid INTEGER PRIMARY KEY, \
    username TEXT, \
    points INTEGER DEFAULT 0, \
    tricks_remaining INTEGER DEFAULT 10, \
    treats_remaining INTEGER DEFAULT 10, \
    tricks_sent INTEGER DEFAULT 0, \
    treats_sent INTEGER DEFAULT 0, \
    tricks_received INTEGER DEFAULT 0, \
    treats_received INTEGER DEFAULT 0)
    """
    sqlconn.execute(CREATION_QUERY)
    sqlconn.execute("CREATE TABLE IF NOT EXISTS submissions (uid INTEGER, cid INTEGER, mid INTEGER, FOREIGN KEY(uid) REFERENCES players(uid) unique (cid, mid))")
    sqlconn.commit()
    sqlconn.close()

def _db_read(user: discord.User | discord.Member, query: tuple) -> list[tuple]:
    sqlconn = sqlite3.connect(DATABASE_PATH)
    # Always try and insert the user, in case they don't yet exist
    sqlconn.execute("INSERT OR IGNORE INTO players (uid, username) VALUES (?, ?)", [user.id, str(user)])
    # The * operator in Python expands a tuple into function params
    results = sqlconn.execute(*query).fetchall()
    sqlconn.close()

    return results

def _db_write(user: discord.User | discord.Member, query: tuple[str, list]):
    sqlconn = sqlite3.connect(DATABASE_PATH)
    # Always try and insert the user, in case they don't yet exist
    sqlconn.execute("INSERT OR IGNORE INTO players (uid, username) VALUES (?, ?)", [user.id, str(user)])
    sqlconn.execute(*query)
    sqlconn.commit()
    sqlconn.close()

def add_submission(message: discord.Message):
    # TODO: Raise some error if entry already exists
    query = ("INSERT INTO submissions (uid, cid, mid) VALUES (?, ?, ?)", [message.author.id, message.channel.id, message.id])
    _db_write(message.author, query)

def change_points(user: discord.User | discord.Member, delta: int):
    query = ("UPDATE players SET points = points + ? WHERE uid = ?", [delta, user.id])
    _db_write(user, query)

def get_player(user: discord.User | discord.Member) -> Player:
    query = ("SELECT points, tricks_remaining, treats_remaining, tricks_sent, treats_sent, tricks_received, treats_received FROM players WHERE uid=?", [user.id])
    results = _db_read(user, query)
    return Player(results[0][0], results[0][1], results[0][2], results[0][3], results[0][4], results[0][5], results[0][6])

def grant_tot(user: discord.Member, num: int):
    query = ("UPDATE players SET tricks_remaining = tricks_remaining + ?, treats_remaining = treats_remaining + ? WHERE uid=?", [num, num, user.id])
    _db_write(user, query)

def has_tot(user: discord.User | discord.Member, tot: Trick_Treat) -> bool:
    player = get_player(user)
    if tot == Trick_Treat.TRICK:
        return player.tricks_remaining != 0
    return player.treats_remaining != 0

def use_tot(user: discord.User | discord.Member, target: discord.User | discord.Member, tot: Trick_Treat):
    if tot == Trick_Treat.TRICK:
        sender_query = ("UPDATE players SET tricks_remaining = tricks_remaining - 1, tricks_sent = tricks_sent + 1 WHERE uid=?", [user.id])
        target_query = ("UPDATE players SET tricks_received = tricks_received + 1 WHERE uid=?", [target.id])
    else:
        sender_query = ("UPDATE players SET treats_remaining = treats_remaining - 1, treats_sent = treats_sent + 1 WHERE uid=?", [user.id])
        target_query = ("UPDATE players SET treats_received = treats_received + 1 WHERE uid=?", [target.id])
    _db_write(user, sender_query)
    _db_write(target, target_query)
