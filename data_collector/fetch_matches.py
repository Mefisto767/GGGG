# data_collector/fetch_matches.py

import os
import json
import requests
from datetime import datetime, timezone

OPEN_DOTA_API_URL = "https://api.opendota.com/api/proMatches"
MATCH_DETAILS_URL = "https://api.opendota.com/api/matches/"

DATA_DIR = os.path.dirname(__file__)
OUT_PATH = os.path.join(DATA_DIR, "matches.json")
MAX_MATCHES = 1000


def fetch_pro_matches():
    response = requests.get(OPEN_DOTA_API_URL)
    response.raise_for_status()
    return response.json()


def fetch_match_details(match_id):
    url = MATCH_DETAILS_URL + str(match_id)
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()


def extract_match_info(match_data):
    try:
        radiant_team = match_data.get("radiant_name")
        dire_team = match_data.get("dire_name")
        if not radiant_team or not dire_team:
            return None

        radiant_win = match_data.get("radiant_win")
        players = match_data.get("players", [])
        if len(players) < 10:
            return None

        radiant_picks = sorted([
            p["hero_id"] for p in players if p.get("isRadiant") and not p.get("leaver_status")
        ])
        dire_picks = sorted([
            p["hero_id"] for p in players if not p.get("isRadiant") and not p.get("leaver_status")
        ])
        if len(radiant_picks) != 5 or len(dire_picks) != 5:
            return None

        return {
            "timestamp": datetime.fromtimestamp(match_data["start_time"], tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
            "start_time": match_data["start_time"],
            "match_id": match_data["match_id"],
            "team_a": radiant_team,
            "team_b": dire_team,
            "team_a_heroes": radiant_picks,
            "team_b_heroes": dire_picks,
            "actual_winner": radiant_team if radiant_win else dire_team,
            "radiant_team": radiant_team,
            "dire_team": dire_team,
            "duration": match_data.get("duration")
        }
    except Exception:
        return None


def load_existing_matches():
    if not os.path.exists(OUT_PATH):
        return []
    with open(OUT_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_matches(matches):
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(matches, f, indent=2, ensure_ascii=False)


def update_matches():
    all_matches = load_existing_matches()
    known_ids = {m["match_id"] for m in all_matches}
    new_matches = []

    print("🔍 Получаю список матчей...")
    for match_summary in fetch_pro_matches():
        match_id = match_summary["match_id"]
        if match_id in known_ids:
            continue

        match_data = fetch_match_details(match_id)
        if not match_data:
            continue

        match_info = extract_match_info(match_data)
        if match_info:
            print(f"✅ Обработан матч {match_id}")
            new_matches.append(match_info)

        if len(all_matches) + len(new_matches) >= MAX_MATCHES:
            break

    all_matches.extend(new_matches)
    save_matches(all_matches)
    print(f"🟢 Обновлено: {len(new_matches)} новых матчей, всего сохранено: {len(all_matches)}")


if __name__ == "__main__":
    update_matches()
