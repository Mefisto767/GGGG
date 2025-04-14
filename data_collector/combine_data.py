import os
import json
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "..", "logs", "match_log.csv")
JSON_PATH = os.path.join(BASE_DIR, "matches.json")
OUT_PATH = os.path.join(BASE_DIR, "combined_matches.csv")

print("📥 Загрузка CSV и JSON...")

df_log = pd.read_csv(LOG_PATH) if os.path.exists(LOG_PATH) else pd.DataFrame()
json_df = pd.DataFrame()

if os.path.exists(JSON_PATH):
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        matches = json.load(f)
    json_df = pd.DataFrame(matches)

    # Normalize winner
    json_df["actual_winner"] = json_df.apply(
        lambda row: row["radiant_team"] if row["actual_winner"] == "Radiant" else row["dire_team"],
        axis=1
    )

    json_df = json_df[["match_id", "actual_winner", "team_a_heroes", "team_b_heroes"]]

# Merge if log not empty
if not df_log.empty:
    df_combined = df_log.copy()

    if not json_df.empty:
        df_combined = df_combined.merge(json_df, on="match_id", how="left", suffixes=("", "_json"))

        for col in ["actual_winner", "team_a_heroes", "team_b_heroes"]:
            json_col = f"{col}_json"
            if json_col in df_combined.columns:
                df_combined[col] = df_combined[col].combine_first(df_combined[json_col])
                df_combined.drop(columns=[json_col], inplace=True)

else:
    df_combined = json_df.copy()

print("💾 Сохранение...")
df_combined.to_csv(OUT_PATH, index=False, encoding="utf-8")
print(f"✅ Объединённый файл сохранён в {OUT_PATH}")
