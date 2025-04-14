import requests
import json
import os
from bs4 import BeautifulSoup

def fetch_winrates_from_protracker():
    url = "https://www.dota2protracker.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", {"id": "hero-stats-table"})
    rows = table.find_all("tr")[1:]  # Пропускаем заголовок

    hero_power = {}

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        hero_name = cols[0].text.strip()
        winrate_text = cols[3].text.strip().replace("%", "")
        try:
            winrate = float(winrate_text)
            power = round((winrate - 40) / 2)  # нормализация в диапазоне ~1–10
            power = max(1, min(power, 10))     # ограничим от 1 до 10
            hero_power[hero_name] = power
        except ValueError:
            continue

    return hero_power

def save_winrates():
    data = fetch_winrates_from_protracker()
    path = os.path.join(os.path.dirname(__file__), "hero_power.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"✅ Сохранено {len(data)} героев в hero_power.json")

if __name__ == "__main__":
    save_winrates()
