# data_collector/combine_data.py

import os
import json
import pandas as pd
import joblib
from datetime import datetime
from collections import defaultdict

ROOT = os.path.dirname(__file__)
CSV_PATH = os.path.join(ROOT, "combined_matches.csv")
MATCH_JSON_PATH = os.path.join(ROOT, "matches.json")
LOG_PATH = os.path.join(ROOT, "filtered_matches_log.csv")
HERO_POWER_PATH = os.path.join(ROOT, "..", "ml", "data", "hero_power.pkl")
HERO_SYNERGY_PATH = os.path.join(ROOT, "..", "ml", "data", "hero_synergy.pkl")


def is_valid_match(row, log_reasons, idx):
    if not isinstance(row["team_a_heroes"], list) or len(row["team_a_heroes"]) != 5:
        log_reasons["invalid_team_a"].append(idx)
        return False
    if not isinstance(row["team_b_heroes"], list) or len(row["team_b_heroes"]) != 5:
        log_reasons["invalid_team_b"].append(idx)
        return False
    if pd.isna(row["actual_winner"]) or row["actual_winner"] not in [row["team_a"], row["team_b"]]:
        log_reasons["missing_winner"].append(idx)
        return False
    return True


def enrich(row, hero_power, hero_synergy):
    def avg_power(hero_list):
        return sum(hero_power.get(str(h), 0) for h in hero_list) / len(hero_list)

    def synergy(hero_list):
        total = 0
        for i in range(len(hero_list)):
            for j in range(i + 1, len(hero_list)):
                total += hero_synergy.get(str(tuple(sorted([hero_list[i], hero_list[j]]))), 0)
        return total

    row["team_a_power"] = avg_power(row["team_a_heroes"])
    row["team_b_power"] = avg_power(row["team_b_heroes"])
    row["team_a_synergy"] = synergy(row["team_a_heroes"])
    row["team_b_synergy"] = synergy(row["team_b_heroes"])
    return row


def main():
    print("📥 Загрузка CSV и JSON...")
    df_csv = pd.read_csv(CSV_PATH) if os.path.exists(CSV_PATH) else pd.DataFrame()
    with open(MATCH_JSON_PATH, "r", encoding="utf-8") as f:
        match_data = json.load(f)
    df_json = pd.DataFrame(match_data)

    print("⚙️ Объединение...")
    combined_df = pd.concat([df_csv, df_json], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset="match_id", keep="last")

    print("⚙️ Обогащение силами и синергией...")
    hero_power = joblib.load(HERO_POWER_PATH)
    hero_synergy = joblib.load(HERO_SYNERGY_PATH)

    log_reasons = defaultdict(list)
    valid_rows = []

    for idx, row in combined_df.iterrows():
        if is_valid_match(row, log_reasons, idx):
            enriched = enrich(row, hero_power, hero_synergy)
            valid_rows.append(enriched)

    final_df = pd.DataFrame(valid_rows)
    final_df = final_df.sort_values(by="start_time", ascending=False).head(100)
    final_df.to_csv(CSV_PATH, index=False)
    print(f"💾 Сохранение {len(final_df)} матчей в: {CSV_PATH}")

    print("🧹 Пропущено по причинам:")
    for reason, indices in log_reasons.items():
        print(f"   ❌ {reason}: {len(indices)}")

    log_rows = []
    for reason, ids in log_reasons.items():
        for idx in ids:
            row = combined_df.iloc[idx].to_dict()
            row["reason"] = reason
            log_rows.append(row)

    pd.DataFrame(log_rows).to_csv(LOG_PATH, index=False)
    print(f"📄 Лог сохранён в: {LOG_PATH}")


if __name__ == "__main__":
    main()
