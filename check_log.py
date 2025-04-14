import json

with open("data_collector/matches.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for d in data[:5]:
    print(d["match_id"], d.get("team_a_heroes"), d.get("team_b_heroes"), d.get("actual_winner"))
