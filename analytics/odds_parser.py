import requests
from bs4 import BeautifulSoup

def get_odds(team_a, team_b):
    url = "https://cyber.sports.ru/dota2/match/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        matches = soup.find_all("a", class_="match__item")

        for block in matches:
            names = block.find_all("div", class_="match__team-name")
            if len(names) < 2:
                continue

            team1 = names[0].get_text(strip=True).lower()
            team2 = names[1].get_text(strip=True).lower()

            if team_a.lower() in team1 and team_b.lower() in team2 or team_a.lower() in team2 and team_b.lower() in team1:
                odds_text = block.find_all("span", class_="match__bet-coef")
                if len(odds_text) >= 2:
                    return float(odds_text[0].text.replace(",", ".")), float(odds_text[1].text.replace(",", "."))
                break

    except Exception as e:
        print(f"❌ Ошибка парсинга кэфов: {e}")

    return None, None
