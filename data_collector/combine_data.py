import os
import json
import pandas as pd
import joblib
from ml.features.hero_stats import get_team_power, get_team_synergy

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(PROJECT_ROOT, "data_collector", "match_log.json")
CSV_PATH = os.path.join(PROJECT_ROOT, "data_collector", "match_log.csv")
OUT_PATH = os.path.join(PROJECT_ROOT, "data_collector", "combined_matches.csv")

def load_json():
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_csv():
    return pd.read_csv(CSV_PATH)

def safe_eval(val):
    try:
        return eval(val) if isinstance(val, str) and val.startswith("[") else []
    except:
        return []

def main():
    print("📥 Загрузка CSV и JSON...")

    json_data = load_json()
    csv_data = load_csv()

    df_json = pd.DataFrame(json_data)
    df_csv = csv_data

    combined_df = pd.concat([df_csv, df_json], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=["match_id"], keep="last")

    combined_df["team_a_heroes"] = combined_df["team_a_heroes"].apply(safe_eval)
    combined_df["team_b_heroes"] = combined_df["team_b_heroes"].apply(safe_eval)

    hero_power = joblib.load(os.path.join(PROJECT_ROOT, "ml", "data", "hero_power.pkl"))
    hero_synergy = joblib.load(os.path.join(PROJECT_ROOT, "ml", "data", "hero_synergy.pkl"))

    def enrich(row):
        a = row.get("team_a_heroes", [])
        b = row.get("team_b_heroes", [])
        return pd.Series({
            "team_a_power": get_team_power(a, hero_power),
            "team_b_power": get_team_power(b, hero_power),
            "team_a_synergy": get_team_synergy(a, hero_synergy),
            "team_b_synergy": get_team_synergy(b, hero_synergy),
        })

    enriched = combined_df.apply(enrich, axis=1)
    combined_df = pd.concat([combined_df, enriched], axis=1)

    print("💾 Сохранение...")
    combined_df.to_csv(OUT_PATH, index=False, encoding="utf-8-sig")
    print(f"✅ Объединённый файл сохранён в {OUT_PATH}")

if __name__ == "__main__":
    main()
