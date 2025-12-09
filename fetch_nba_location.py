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