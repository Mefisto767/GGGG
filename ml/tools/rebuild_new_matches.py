import os
import json
from datetime import datetime

# 📁 Путь до корня проекта (где находится run_daily.py)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MATCHES_FILE = os.path.join(PROJECT_ROOT, 'data_collector', 'matches.json')
NEW_MATCHES_FILE = os.path.join(PROJECT_ROOT, 'data_collector', 'new_matches.json')
MATCH_LOG_FILE = os.path.join(PROJECT_ROOT, 'logs', 'match_log.csv')

# Загрузка старых матчей
with open(MATCHES_FILE, encoding='utf-8') as f:
    all_matches = json.load(f)

# Загрузка матчей из match_log.csv
import pandas as pd
match_log_df = pd.read_csv(MATCH_LOG_FILE)
used_ids = set(match_log_df['match_id'].dropna().astype(str))

# Фильтрация новых матчей по match_id и duration > 15 минут
filtered_matches = [
    m for m in all_matches
    if str(m['match_id']) not in used_ids and m.get("duration", 0) > 900
]

# Сохранение отфильтрованных
os.makedirs(os.path.dirname(NEW_MATCHES_FILE), exist_ok=True)
def save_new_matches(matches):
    with open(NEW_MATCHES_FILE, 'w', encoding='utf-8') as f:
        json.dump(matches, f, indent=2, ensure_ascii=False)

save_new_matches(filtered_matches)
print(f"✅ Сохранено новых матчей: {len(filtered_matches)}")
