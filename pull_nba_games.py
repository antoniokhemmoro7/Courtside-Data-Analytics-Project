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

# Insert cleaned game-level data into SQLite
def insert_games(df):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Group rows by GAME_ID to combine home/away records
    grouped = df.groupby("GAME_ID")

    total_inserted = 0

    for game_id, group in grouped:
        # Skip anything that isn't a clean 2-row game
        if len(group) != 2:
            continue

        row1, row2 = group.iloc[0], group.iloc[1]

        # MATCHUP tells us who was home vs away
        if "@" in row1["MATCHUP"]:
            away_row = row1
            home_row = row2
        else:
            away_row = row2
            home_row = row1

        # Extract cleaned values
        date = home_row["GAME_DATE"]
        home_team = home_row["TEAM_NAME"]
        away_team = away_row["TEAM_NAME"]
        home_score = int(home_row["PTS"])
        away_score = int(away_row["PTS"])

        # Insert or update game in DB
        cur.execute("""
            INSERT OR REPLACE INTO games
            (game_id, date, home_team, away_team, home_score, away_score)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (game_id, date, home_team, away_team, home_score, away_score))

        total_inserted += 1

    conn.commit()
    conn.close()

    print(f"Inserted {total_inserted} total games into database!")

# main
if __name__ == "__main__":
    create_table()
    df = fetch_games()
    insert_games(df)
