from nba_api.stats.endpoints import LeagueGameFinder
import sqlite3
import pandas as pd

DB_NAME = "nba.db"


# Create the games table
def create_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS games (
            game_id TEXT PRIMARY KEY,
            date TEXT,
            home_team TEXT,
            away_team TEXT,
            home_score INTEGER,
            away_score INTEGER
        )
    """)

    conn.commit()
    conn.close()
