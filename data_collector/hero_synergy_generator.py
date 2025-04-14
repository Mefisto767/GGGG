import json
import requests
from collections import defaultdict
from itertools import combinations

def get_matches(num_matches=1000):
    url = f"https://api.opendota.com/api/proMatches"
    response = requests.get(url)
    return response.json()[:num_matches]

def get_draft(match_id):
    url = f"https://api.opendota.com/api/matches/{match_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    picks = []
    try:
        for pick in data.get("picks_bans", []):
            if pick.get("is_pick") and pick.get("team") == (0 if data["radiant_win"] else 1):
                picks.append(pick["hero_id"])
    except:
        return None

    return picks

def generate_synergy():
    synergy = defaultdict(lambda: {"wins": 0, "games": 0})

    matches = get_matches(500)

    for match in matches:
        match_id = match["match_id"]
        draft = get_draft(match_id)
        if not draft or len(draft) < 5:
            continue

        pairs = combinations(sorted(draft), 2)
        for pair in pairs:
            synergy[pair]["wins"] += 1
            synergy[pair]["games"] += 1

    # Посчитать винрейт
    synergy_final = {}
    for pair, stats in synergy.items():
        winrate = stats["wins"] / stats["games"] if stats["games"] > 0 else 0
        synergy_final[str(pair)] = round(winrate, 3)

    # Сохранить файл в ту же папку
    import os
    BASE_DIR = os.path.dirname(__file__)
    output_path = os.path.join(BASE_DIR, "hero_synergy.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(synergy_final, f, ensure_ascii=False, indent=2)

    print(f"✅ Синергия сохранена. Уникальных пар: {len(synergy_final)}")

if __name__ == "__main__":
    generate_synergy()
