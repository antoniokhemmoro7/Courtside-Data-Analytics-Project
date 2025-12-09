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

    # Pull the full 2024–25 season from nba_api
def fetch_games():
    print("Fetching NBA 2024-25 season games from nba_api...")

    # LeagueGameFinder returns two rows per game (home + away)
    gamefinder = LeagueGameFinder(season_nullable="2024-25")
    df = gamefinder.get_data_frames()[0]

    print(f"Total rows fetched: {len(df)}")
    return df

