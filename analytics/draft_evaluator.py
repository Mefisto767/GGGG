import json
import os

# Абсолютный путь к JSON-файлу с power-оценками героев
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
POWER_PATH = os.path.join(BASE_DIR, "data_collector", "hero_power.json")


# Функция оценки силы команды
def calculate_team_power(pick: list[str], hero_power: dict) -> int:
    return sum(hero_power.get(hero, 0) for hero in pick)


# Главная функция, которую используют другие модули
def evaluate_draft(team_a: list[str], team_b: list[str]) -> tuple[int, int]:
    with open(POWER_PATH, encoding="utf-8") as f:
        hero_power = json.load(f)

    a_power = calculate_team_power(team_a, hero_power)
    b_power = calculate_team_power(team_b, hero_power)

    return a_power, b_power


# Пример ручного запуска
if __name__ == "__main__":
    team_a = ["Pudge", "Drow Ranger", "Lina", "Zeus", "Crystal Maiden"]
    team_b = ["Juggernaut", "Shadow Shaman", "Tiny", "Windranger", "Sven"]

    a_score, b_score = evaluate_draft(team_a, team_b)
    print(f"Team A: {a_score}, Team B: {b_score}")
