import sqlite3

from dataclasses import dataclass

from config import DATABASE_PATH
from utils import Trick_Treat

@dataclass
class Player:
    uid: int
    points: int
    tricks: int
    treats: int

def initialize():
    sqlconn = sqlite3.connect(DATABASE_PATH)
    # TODO: Figure out how to pass in the default values here
    sqlconn.execute("CREATE TABLE IF NOT EXISTS players (uid INTEGER PRIMARY KEY, points INTEGER DEFAULT 0, tricks INTEGER DEFAULT 10, treats INTEGER DEFAULT 10)")
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
    query = ("SELECT points, tricks, treats FROM players WHERE uid=?", [uid])
    results = _db_read(uid, query)
    return Player(uid, results[0][0], results[0][1], results[0][2])

def has_tot(uid: int, tot: Trick_Treat) -> bool:
    player = get_player(uid)
    if tot == Trick_Treat.TRICK:
        return player.tricks != 0
    return player.treats != 0

def use_tot(uid: int, tot: Trick_Treat):
    if tot == Trick_Treat.TRICK:
        query = ("UPDATE players SET tricks = tricks - 1 WHERE uid=?", [uid])
    else:
        query = ("UPDATE players SET treats = treats - 1 WHERE uid=?", [uid])
    _db_write(uid, query)
