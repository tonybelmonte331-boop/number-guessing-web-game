# Fantasy Football Player Ranker

players = [
    {
        "name": "Christian McCaffrey",
        "position": "RB",
        "rush_yards": 90,
        "rush_tds": 1,
        "receptions": 6,
        "rec_yards": 40,
        "rec_tds": 0
    },
    {
        "name": "Tyreek Hill",
        "position": "WR",
        "rush_yards": 0,
        "rush_tds": 0,
        "receptions": 8,
        "rec_yards": 110,
        "rec_tds": 1
    }
]

def calculate_points(player):
    points = 0
    points += player["rush_yards"] * 0.1
    points += player["rush_tds"] * 6
    points += player["receptions"] * 1
    points += player["rec_yards"] * 0.1
    points += player["rec_tds"] * 6
    return points

for player in players:
    player["points"] = calculate_points(player)

players.sort(key=lambda x: x["points"], reverse=True)

print("Fantasy Rankings:")
for rank, player in enumerate(players, start=1):
    print(f"{rank}. {player['name']} - {player['points']} pts")
