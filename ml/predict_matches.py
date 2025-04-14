# ml/predict_matches.py

import os
import json
import pandas as pd
from datetime import datetime
from ml.predictor import predict_winner

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MATCH_LOG = os.path.join(BASE_DIR, "logs", "match_log.csv")
NEW_MATCHES = os.path.join(BASE_DIR, "data_collector", "new_matches.json")
OUTPUT_PATH = os.path.join(BASE_DIR, "analytics", "predictions_log.csv")

def main():
    if not os.path.exists(NEW_MATCHES):
        print("⚠️ Нет файла новых матчей.")
        return

    with open(NEW_MATCHES, "r", encoding="utf-8") as f:
        matches = json.load(f)

    if not matches:
        print("ℹ️ Нет новых матчей для предсказания.")
        return

    # исторические матчи
    match_log = pd.read_csv(MATCH_LOG)

    results = []

    for match in matches:
        team_a = match["team_a"]
        team_b = match["team_b"]
        picks_a = match["picks_a"]
        picks_b = match["picks_b"]
        match_id = match.get("match_id", "")

        result = predict_winner(team_a, team_b, picks_a, picks_b, match_log)
        result.update({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "match_id": match_id,
            "team_a": team_a,
            "team_b": team_b
        })

        print("✅", result)
        results.append(result)

    df_result = pd.DataFrame(results)
    df_result.to_csv(OUTPUT_PATH, index=False)
    print(f"📦 Сохранено {len(results)} предсказаний в {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
