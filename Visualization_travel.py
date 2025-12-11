import matplotlib.pyplot as plt
import sqlite3
# Load travel results
def load_results():
    # Load ONLY the 30 NBA teams
    conn = sqlite3.connect("nba.db")
    cur = conn.cursor()
    cur.execute("SELECT name FROM teams")
    official_teams = {row[0] for row in cur.fetchall()}
    conn.close()

    results = {}

    with open("team_travel_results.txt", "r") as f:
        lines = f.readlines()[3:]  # skip header

        for line in lines:
            if ": " in line:
                team, miles = line.strip().split(": ")
                miles = float(miles.replace(" miles", ""))

                # only keep REAL NBA teams
                if team in official_teams:
                    results[team] = miles

    return results


def create_bar_chart(results):
    # Sort teams by miles traveled (descending)
    teams = list(results.keys())
    miles = list(results.values())

    # Sort both lists together
    teams, miles = zip(*sorted(zip(teams, miles), key=lambda x: x[1], reverse=True))

    plt.figure(figsize=(14, 8))
    plt.bar(teams, miles, color="skyblue", edgecolor="black")
    plt.xticks(rotation=90)
    plt.ylabel("Total Miles Traveled")
    plt.title("NBA Team Travel Distance (2024–25 Season)")

    plt.tight_layout()
    plt.savefig("travel_distance_bar_chart.png")
    plt.close()

    print("Saved chart: travel_distance_bar_chart.png")


if __name__ == "__main__":
    travel_results = load_results()
    create_bar_chart(travel_results)
