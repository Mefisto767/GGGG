import json
import os

def evaluate_value(match, predicted_winner, predicted_prob):
    try:
        path = os.path.join(os.path.dirname(__file__), "../data_collector/odds.json")
        with open(path, "r", encoding="utf-8") as file:
            odds = json.load(file)

        coef = odds.get(predicted_winner)
        if not coef:
            return {
                "value": False,
                "comment": "Нет коэффициента для команды"
            }

        implied_prob = 1 / coef * 100  # Преобразуем кэф в %
        delta = predicted_prob - implied_prob

        if delta >= 8:
            return {
                "value": True,
                "comment": f"Value есть! Наша вероятность: {predicted_prob}%, у букмекера: {round(implied_prob)}%"
            }
        else:
            return {
                "value": False,
                "comment": f"Value нет. Наша вероятность: {predicted_prob}%, у букмекера: {round(implied_prob)}%"
            }

    except Exception as e:
        return {
            "value": False,
            "comment": f"Ошибка при анализе value: {e}"
        }
