import sqlite3
import time
import requests

DB_NAME = "nba.db"

# Arena names mapped to teams — avoids geocoding errors
ARENA_MAP = {
    "Atlanta Hawks": "State Farm Arena, Atlanta, GA",
    "Boston Celtics": "TD Garden, Boston, MA",
    "Brooklyn Nets": "Barclays Center, Brooklyn, NY",
    "Charlotte Hornets": "Spectrum Center, Charlotte, NC",
    "Chicago Bulls": "United Center, Chicago, IL",
    "Cleveland Cavaliers": "Rocket Mortgage FieldHouse, Cleveland, OH",
    "Dallas Mavericks": "American Airlines Center, Dallas, TX",
    "Denver Nuggets": "Ball Arena, Denver, CO",
    "Detroit Pistons": "Little Caesars Arena, Detroit, MI",
    "Golden State Warriors": "Chase Center, San Francisco, CA",
    "Houston Rockets": "Toyota Center, Houston, TX",
    "Indiana Pacers": "Gainbridge Fieldhouse, Indianapolis, IN",
    "LA Clippers": "Crypto.com Arena, Los Angeles, CA",
    "Los Angeles Lakers": "Crypto.com Arena, Los Angeles, CA",
    "Memphis Grizzlies": "FedExForum, Memphis, TN",
    "Miami Heat": "Kaseya Center, Miami, FL",
    "Milwaukee Bucks": "Fiserv Forum, Milwaukee, WI",
    "Minnesota Timberwolves": "Target Center, Minneapolis, MN",
    "New Orleans Pelicans": "Smoothie King Center, New Orleans, LA",
    "New York Knicks": "Madison Square Garden, New York, NY",
    "Oklahoma City Thunder": "Paycom Center, Oklahoma City, OK",
    "Orlando Magic": "Kia Center, Orlando, FL",
    "Philadelphia 76ers": "Wells Fargo Center, Philadelphia, PA",
    "Phoenix Suns": "Mortgage Matchup Center, Phoenix, AZ",
    "Portland Trail Blazers": "Moda Center, Portland, OR",
    "Sacramento Kings": "Golden 1 Center, Sacramento, CA",
    "San Antonio Spurs": "Frost Bank Center, San Antonio, TX",
    "Toronto Raptors": "Scotiabank Arena, Toronto, ON",
    "Utah Jazz": "Delta Center, Salt Lake City, UT",
    "Washington Wizards": "Capital One Arena, Washington, DC"
}

def create_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS team_locations (
            team_id INTEGER PRIMARY KEY,
            team_name TEXT,
            arena TEXT,
            latitude REAL,
            longitude REAL
        )
    """)

    conn.commit()
    conn.close()


def geocode_address(address):
    """Use free Nominatim geocoding to get GPS coordinates."""
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }

    response = requests.get(url, params=params, headers={"User-Agent": "SI201 Project"})
    data = response.json()

    if len(data) == 0:
        return None, None

    return float(data[0]["lat"]), float(data[0]["lon"])


def insert_team_location(team_id, name, arena, lat, lon):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        INSERT OR REPLACE INTO team_locations
        (team_id, team_name, arena, latitude, longitude)
        VALUES (?, ?, ?, ?, ?)
    """, (team_id, name, arena, lat, lon))

    conn.commit()
    conn.close()


def fetch_and_store_locations():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT team_id, name FROM teams")
    teams = cur.fetchall()
    conn.close()

    print(f"Found {len(teams)} teams. Starting geocoding...\n")

    for team_id, team_name in teams:
        arena = ARENA_MAP[team_name]

        print(f"Geocoding: {team_name} → {arena}")

        lat, lon = geocode_address(arena)

        if lat is None:
            print(f"Could not find coordinates for {team_name}. Skipping.")
            continue

        insert_team_location(team_id, team_name, arena, lat, lon)

        print(f"✓ Saved {team_name}: ({lat}, {lon})")
        time.sleep(1)  # Nominatim rate limit

    print("\nAll team locations saved successfully!")


if __name__ == "__main__":
    create_table()
    fetch_and_store_locations()
