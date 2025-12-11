import sqlite3
import math

DB_NAME = "nba.db"

# Haversine distance (miles)
def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (math.sin(dphi/2)**2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Load team locations (team_name -> lat/lon)
def load_team_locations():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("SELECT team_name, latitude, longitude FROM team_locations")
    locations = {row[0]: (row[1], row[2]) for row in cur.fetchall()}

    conn.close()
    return locations


# Load games from the 2024-25 season
def load_games():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT game_id, date, home_team, away_team
        FROM games
        ORDER BY date
    """)

    games = cur.fetchall()
    conn.close()
    return games


# Build schedules (team_name -> list of dates/arenas)
def build_team_schedules(games):
    schedules = {}

    for game_id, date, home_team, away_team in games:

        # Home team plays at home arena
        schedules.setdefault(home_team, []).append((date, game_id, True))

        # Away team travels to home arena
        schedules.setdefault(away_team, []).append((date, game_id, False))

    # Sort by date
    for team in schedules:
        schedules[team].sort(key=lambda x: x[0])

    return schedules

# Compute total miles traveled per team
def compute_travel(schedules, team_locations, games):

    # Map each game ... arena (home team name)
    game_arenas = {}
    for game_id, date, home_team, away_team in games:
        game_arenas[game_id] = home_team

    results = {}

    for team, schedule in schedules.items():
        total_miles = 0
        prev_lat, prev_lon = None, None

        for date, game_id, is_home in schedule:
            arena_team = game_arenas[game_id]  # game played at home team’s city

            if arena_team not in team_locations:
                continue

            lat, lon = team_locations[arena_team]

            if prev_lat is not None:
                total_miles += haversine(prev_lat, prev_lon, lat, lon)

            prev_lat, prev_lon = lat, lon

        results[team] = total_miles

    return results

# Save results
def save_results(results):
    with open("team_travel_results.txt", "w") as f:
        f.write("NBA Team Travel Distance (2024–25 Season)\n")
        f.write("---------------------------------------------------\n\n")

        for team, miles in sorted(results.items(), key=lambda x: x[1], reverse=True):
            f.write(f"{team}: {miles:.2f} miles\n")

    print("Saved results to team_travel_results.txt")

# MAIN
if __name__ == "__main__":
    print("Loading games & locations...")
    games = load_games()
    locations = load_team_locations()
    schedules = build_team_schedules(games)

    print("Calculating travel distances...")
    results = compute_travel(schedules, locations, games)

    save_results(results)
    print("Done.")
