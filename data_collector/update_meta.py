import os
import requests
import json

def fetch_winrate_from_opendota():
    url = "https://api.opendota.com/api/heroStats"
    response = requests.get(url)
    data = response.json()

    hero_power = {}
    for hero in data:
        name = hero.get("localized_name")
        pro_pick = hero.get("pro_pick", 0)
        pro_win = hero.get("pro_win", 0)

        winrate = (pro_win / pro_pick * 100) if pro_pick > 0 else 47
        power = round((winrate - 40) / 2)
        power = max(1, min(power, 10))

        hero_power[name] = power

    return hero_power

def update_hero_power():
    data = fetch_winrate_from_opendota()
    path = os.path.join(os.path.dirname(__file__), "hero_power.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Мета обновлена. Обновлено {len(data)} героев.")

if __name__ == "__main__":
    update_hero_power()
