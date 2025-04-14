import os
import sys
import pandas as pd
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(PROJECT_ROOT)

from analytics.predictor import make_predictions
from ml.tools.rebuild_csv_from_json import rebuild_from_json

LOG_PATH = os.path.join(PROJECT_ROOT, 'logs', 'match_log.csv')
NEW_CSV_PATH = os.path.join(PROJECT_ROOT, 'logs', 'new_matches.csv')

def train_model():
    from ml.train_model import train_model
    train_model()

def update_logs():
    if not os.path.exists(NEW_CSV_PATH):
        print("❌ Нет новых матчей для обновления.")
        return

    existing = pd.read_csv(LOG_PATH)
    new_data = pd.read_csv(NEW_CSV_PATH)

    combined = pd.concat([existing, new_data])
    combined = combined.drop_duplicates(subset=['team_a', 'team_b', 'actual_winner'], keep='first')
    combined.to_csv(LOG_PATH, index=False)

    added = max(0, len(combined) - len(existing))
    print(f"✅ Добавлено {added} новых матчей в match_log.csv")

    os.remove(NEW_CSV_PATH)
    train_model()
    print("✅ Модель переобучена.")

def show_stats():
    subprocess.run(["python", os.path.join(PROJECT_ROOT, "analytics", "stats.py")])

if __name__ == "__main__":
    rebuild_from_json()
    update_logs()
    make_predictions()
    show_stats()
