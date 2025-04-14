import os
import sys
import pandas as pd
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from analytics.predictor import make_predictions
from ml.tools.rebuild_csv_from_json import rebuild_from_json
from ml.train_model import train_model

LOG_PATH = os.path.join(PROJECT_ROOT, 'logs', 'match_log.csv')
NEW_CSV_PATH = os.path.join(PROJECT_ROOT, 'logs', 'new_matches.csv')
COMBINED_PATH = os.path.join(PROJECT_ROOT, 'data_collector', 'combined_matches.csv')

def update_logs():
    if not os.path.exists(NEW_CSV_PATH):
        print("❌ Нет новых матчей для обновления.")
        return

    new_data = pd.read_csv(NEW_CSV_PATH)
    if os.path.exists(LOG_PATH):
        existing = pd.read_csv(LOG_PATH)

        # 👇 Объединяем все столбцы, даже если у кого-то не хватает
        all_columns = sorted(set(existing.columns).union(set(new_data.columns)))
        existing = existing.reindex(columns=all_columns)
        new_data = new_data.reindex(columns=all_columns)

        combined = pd.concat([existing, new_data], ignore_index=True)
    else:
        combined = new_data.copy()

    combined = combined.drop_duplicates(subset=['match_id'], keep='first')
    combined.to_csv(LOG_PATH, index=False)

    added = len(new_data)
    print(f"✅ Добавлено {added} новых матчей в match_log.csv")

    os.remove(NEW_CSV_PATH)
    print("🚀 Запускаем повторное обучение...")
    train_model(csv_path=COMBINED_PATH)
    print("✅ Модель переобучена.")

def show_stats():
    subprocess.run(["python", os.path.join(PROJECT_ROOT, "analytics", "stats.py")])

if __name__ == "__main__":
    rebuild_from_json()
    update_logs()
    make_predictions()
    show_stats()
