import sqlite3

from dataclasses import dataclass

from config import DATABASE_PATH
from utils import Trick_Treat

@dataclass
class Player:
    uid: int
    points: int
    tricks_remaining: int
    treats_remaining: int
    tricks_sent: int
    treats_sent: int
    tricks_hit: int
    treats_hit: int


def initialize():
    sqlconn = sqlite3.connect(DATABASE_PATH)
    # TODO: Figure out how to pass in the default values here
    CREATION_QUERY = """
    CREATE TABLE IF NOT EXISTS players (\
    uid INTEGER PRIMARY KEY, \
    points INTEGER DEFAULT 0, \
    tricks_remaining INTEGER DEFAULT 10, \
    treats_remaining INTEGER DEFAULT 10, \
    tricks_sent INTEGER DEFAULT 0, \
    treats_sent INTEGER DEFAULT 0, \
    tricks_hit INTEGER DEFAULT 0, \
    treats_hit INTEGER DEFAULT 0)
    """
    sqlconn.execute(CREATION_QUERY)
    sqlconn.commit()
    sqlconn.close()

def _db_read(uid: int, query: tuple) -> list[tuple]:
    sqlconn = sqlite3.connect(DATABASE_PATH)
    # Always try and insert the user, in case they don't yet exist
    sqlconn.execute("INSERT OR IGNORE INTO players (uid) VALUES (?)", [uid])
    # The * operator in Python expands a tuple into function params
    results = sqlconn.execute(*query).fetchall()
    sqlconn.close()

    return results

def _db_write(uid: int, query: tuple[str, list]):
    sqlconn = sqlite3.connect(DATABASE_PATH)
    # Always try and insert the user, in case they don't yet exist
    sqlconn.execute("INSERT OR IGNORE INTO players (uid) VALUES (?)", [uid])
    sqlconn.execute(*query)
    sqlconn.commit()
    sqlconn.close()

def change_points(uid: int, delta: int):
    query = ("UPDATE players SET points = points + ? WHERE uid = ?", [delta, uid])
    _db_write(uid, query)

def get_player(uid: int) -> Player:
    query = ("SELECT points, tricks_remaining, treats_remaining, tricks_sent, treats_sent, tricks_hit, treats_hit FROM players WHERE uid=?", [uid])
    results = _db_read(uid, query)
    return Player(uid, results[0][0], results[0][1], results[0][2], results[0][3], results[0][4], results[0][5], results[0][6])

def has_tot(uid: int, tot: Trick_Treat) -> bool:
    player = get_player(uid)
    if tot == Trick_Treat.TRICK:
        return player.tricks_remaining != 0
    return player.treats_remaining != 0

def use_tot(uid: int, target: int, tot: Trick_Treat):
    if tot == Trick_Treat.TRICK:
        sender_query = ("UPDATE players SET tricks_remaining = tricks_remaining - 1, tricks_sent = tricks_sent + 1 WHERE uid=?", [uid])
        target_query = ("UPDATE players SET tricks_hit = tricks_hit + 1 WHERE uid=?", [target])
    else:
        sender_query = ("UPDATE players SET treats_remaining = treats_remaining - 1, treats_sent = treats_sent + 1 WHERE uid=?", [uid])
        target_query = ("UPDATE players SET treats_hit = treats_hit + 1 WHERE uid=?", [target])
    _db_write(uid, sender_query)
    _db_write(target, target_query)
