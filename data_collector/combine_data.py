import os
import pandas as pd
import json

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data_collector", "match_log.csv")
JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "data_collector", "matches.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data_collector", "combined_matches.csv")

def load_csv(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        print(f"❌ CSV файл не найден: {path}")
        return pd.DataFrame()
    print("✅ CSV загружен")
    return pd.read_csv(path)

def load_json(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        print(f"❌ JSON файл не найден: {path}")
        return pd.DataFrame()
    print("✅ JSON загружен")
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)

def combine_columns(df, col1, col2, out_col):
    if col1 in df.columns and col2 in df.columns:
        df[out_col] = df[col1].combine_first(df[col2])
    elif col1 in df.columns:
        df[out_col] = df[col1]
    elif col2 in df.columns:
        df[out_col] = df[col2]
    else:
        df[out_col] = pd.NA

def merge_datasets(csv_df: pd.DataFrame, json_df: pd.DataFrame) -> pd.DataFrame:
    if "match_id" not in csv_df.columns:
        csv_df["match_id"] = pd.NA
    if "match_id" not in json_df.columns:
        json_df["match_id"] = pd.NA

    merged = pd.merge(csv_df, json_df, on="match_id", how="outer", suffixes=("", "_json"))

    combine_columns(merged, "team_a", "radiant_team", "team_a")
    combine_columns(merged, "team_b", "dire_team", "team_b")
    combine_columns(merged, "actual_winner", "actual_winner_json", "actual_winner")
    combine_columns(merged, "timestamp", "start_time", "timestamp")

    result = merged[[
        "timestamp", "match_id", "team_a", "team_b",
        "team_a_heroes", "team_b_heroes", "actual_winner"
    ]].dropna(subset=["match_id", "team_a", "team_b", "actual_winner"])

    return result.sort_values("timestamp", ascending=False).reset_index(drop=True)

def save_to_csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)
    print(f"✅ Объединённый файл сохранён в {path}")

def main():
    print("📥 Загрузка CSV и JSON...")
    csv_df = load_csv(CSV_PATH)
    json_df = load_json(JSON_PATH)

    print("🔄 Объединение данных...")
    combined_df = merge_datasets(csv_df, json_df)

    print("💾 Сохранение...")
    save_to_csv(combined_df, OUTPUT_PATH)

if __name__ == "__main__":
    main()
