import os
import json
import pandas as pd

# Абсолютный путь к директории проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Правильные пути
MATCHES_PATH = os.path.join(BASE_DIR, "data_collector", "matches.json")
LOG_CSV_PATH = os.path.join(BASE_DIR, "logs", "match_log.csv")

# Проверка файла
if not os.path.exists(MATCHES_PATH):
    raise FileNotFoundError(f"❌ Файл не найден: {MATCHES_PATH}")

# Загрузка
with open(MATCHES_PATH, "r", encoding="utf-8") as f:
    matches = json.load(f)

parsed = []
for m in matches:
    if all(k in m for k in ["timestamp", "match_id", "team_a", "team_b", "actual_winner"]):
        parsed.append({
            "timestamp": m["timestamp"],
            "match_id": m["match_id"],
            "team_a": m["team_a"],
            "team_b": m["team_b"],
            "predicted_winner": "",
            "confidence": "",
            "value_flag": "",
            "actual_winner": m["actual_winner"]
        })

df_new = pd.DataFrame(parsed)

# Если лог уже существует – дополняем
if os.path.exists(LOG_CSV_PATH):
    df_old = pd.read_csv(LOG_CSV_PATH)
    df_all = pd.concat([df_old, df_new], ignore_index=True)
    df_all.drop_duplicates(subset=["match_id"], inplace=True)
else:
    df_all = df_new

df_all.to_csv(LOG_CSV_PATH, index=False, encoding="utf-8")
print(f"✅ Лог обновлён. Всего матчей: {len(df_all)}")
