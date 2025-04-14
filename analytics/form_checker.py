import json
import os

FORM_DATA_PATH = os.path.join(os.path.dirname(__file__), "../data_collector/player_form.json")

def load_form_data():
    try:
        with open(FORM_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def get_player_form(match):
    try:
        form_data = load_form_data()
        team_a = match.get("team_a")
        team_b = match.get("team_b")

        team_a_form = form_data.get(team_a, 0)
        team_b_form = form_data.get(team_b, 0)

        return {
            "team_a_form": team_a_form,
            "team_b_form": team_b_form
        }
    except Exception as e:
        print(f"[ОШИБКА В ОЦЕНКЕ ФОРМЫ]: {e}")
        return {
            "team_a_form": 0,
            "team_b_form": 0
        }
