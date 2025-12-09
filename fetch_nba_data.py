import requests
import json
import sqlite3

API_KEY = "50f6ec4e-ad29-421b-b19e-3836228cba49"
DB_NAME = "nba.db"

# Pulls the list of NBA teams from the API and returns them in a clean format.
# Filtering is needed because the API includes old/defunct teams.
def get_team_list():
    url = "https://api.balldontlie.io/v1/teams"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.get(url, headers=headers)
    data = response.json()

    teams = []

    for team in data["data"]:
        # Only keep real NBA teams (East or West conference + real division)
        if team["conference"] in ["East", "West"] and team["division"] != "":
            teams.append({
                "team_id": team["id"],
                "name": team["full_name"],
                "city": team["city"],
                "abbreviation": team["abbreviation"]
            })

    return teams


# Saves the cleaned team data into a JSON file.
def save_json(teams):
    with open("teams.json", "w") as file:
        json.dump(teams, file, indent=4)
    print("Saved teams.json")


# Creates the SQL tables if they don't already exist.
def create_tables():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            name TEXT,
            city TEXT,
            abbreviation TEXT
        )
    ''')

    conn.commit()
    conn.close()


# Inserts the team data into the teams table.
# Using OR IGNORE so duplicates do nothing if the script is run multiple times.
def insert_teams(teams):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    for team in teams:
        c.execute("""
            INSERT OR IGNORE INTO teams (team_id, name, city, abbreviation)
            VALUES (?, ?, ?, ?)
        """, (team["team_id"], team["name"], team["city"], team["abbreviation"]))

    conn.commit()
    conn.close()

    print(f"Inserted {len(teams)} teams into nba.db")


# Runs the whole pipeline: pull data, save it, set up the DB, insert rows.
if __name__ == "__main__":
    teams = get_team_list()
    print("Pulled", len(teams), "NBA teams.")

    save_json(teams)
    create_tables()
    insert_teams(teams)
