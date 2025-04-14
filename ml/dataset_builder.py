import pandas as pd
import json
from ml.power_calculator import calculate_team_power


def build_dataset():
    """
    Строим обучающий датасет (X, y) для модели
    :return: X (features), y (labels)
    """
    with open("data_collector/hero_power.json", encoding="utf-8") as f:
        hero_power = json.load(f)

    df = pd.read_csv("match_log.csv", encoding="utf-8")

    data = []

    for _, row in df.iterrows():
        try:
            radiant_team = row['radiant_team'].split('|')
            dire_team = row['dire_team'].split('|')

            radiant_power = calculate_team_power(radiant_team, hero_power)
            dire_power = calculate_team_power(dire_team, hero_power)

            features = {
                "radiant_power": radiant_power,
                "dire_power": dire_power
            }

            label = 1 if row["winner"] == "Radiant" else 0

            data.append((features, label))

        except Exception as e:
            print(f"⚠️ Ошибка в матче {row.get('match_id', 'N/A')}: {e}")

    X = [x for x, _ in data]
    y = [y for _, y in data]

    return pd.DataFrame(X), y


def build_dataset_for_prediction(matches=None):
    """
    Подготовка датасета для предсказаний.
    :param matches: список словарей матчей (id, radiant_team, dire_team)
    :return: X_pred, matches_info
    """
    with open("data_collector/hero_power.json", encoding="utf-8") as f:
        hero_power = json.load(f)

    X_pred = []
    matches_info = []

    for match in matches:
        try:
            radiant_team = match['radiant_team'].split('|')
            dire_team = match['dire_team'].split('|')

            radiant_power = calculate_team_power(radiant_team, hero_power)
            dire_power = calculate_team_power(dire_team, hero_power)

            X_pred.append({
                "radiant_power": radiant_power,
                "dire_power": dire_power
            })
            matches_info.append(match)

        except Exception as e:
            print(f"⚠️ Ошибка в предсказании матча {match.get('match_id', 'N/A')}: {e}")

    return pd.DataFrame(X_pred), matches_info
