import requests
import json
import os

def fetch_winrate_from_opendota():
    url = "https://api.opendota.com/api/heroStats"
    response = requests.get(url)
    data = response.json()

    hero_power = {}

    for hero in data:
        name = hero.get("localized_name")
        winrate = (hero["pro_win"] / hero["pro_pick"] * 100) if hero["pro_pick"] > 0 else 45

        # Преобразуем winrate в силу (от 1 до 10)
        power = round((winrate - 40) / 2)
        power = max(1, min(power, 10))

        hero_power[name] = power

    return hero_power

def save_winrate_to_json():
    power_data = fetch_winrate_from_opendota()
    path = os.path.join(os.path.dirname(__file__), "hero_power.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(power_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Сохранено {len(power_data)} героев в hero_power.json")

if __name__ == "__main__":
    save_winrate_to_json()
