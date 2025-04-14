# 📁 analytics/auto_predictor.py
import os
import json
import pandas as pd
import logging
from datetime import datetime
from ml.train_model import train_model
from ml.prepare_data import encode_match
from joblib import load

# Пути
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEW_MATCHES_PATH = os.path.join(PROJECT_ROOT, 'data_collector', 'new_matches.json')
PREDICTIONS_LOG_PATH = os.path.join(PROJECT_ROOT, 'logs', 'match_log.csv')
MODEL_PATH = os.path.join(PROJECT_ROOT, 'models', 'model.joblib')
ENCODER_PATH = os.path.join(PROJECT_ROOT, 'models', 'encoder.joblib')

logging.basicConfig(level=logging.INFO, format="%(message)s")

# Загружаем матчи
if not os.path.exists(NEW_MATCHES_PATH):
    logging.warning("⚠️ Нет новых матчей для предсказания.")
    exit()

with open(NEW_MATCHES_PATH, 'r', encoding='utf-8') as f:
    new_matches = json.load(f)

if not new_matches:
    logging.info("ℹ️ Новых матчей нет.")
    exit()

logging.info("🔁 Проверка и автообучение модели...")
train_model()
model = load(MODEL_PATH)
encoder = load(ENCODER_PATH)

predictions = []

for match in new_matches:
    X = encode_match(match, encoder)
    proba = model.predict_proba([X])[0]
    predicted = model.predict([X])[0]
    confidence = round(max(proba), 2)

    record = {
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "match_id": match['match_id'],
        "team_a": match['radiant_team'],
        "team_b": match['dire_team'],
        "team_a_heroes": match.get("team_a_heroes", []),
        "team_b_heroes": match.get("team_b_heroes", []),
        "predicted_winner": predicted,
        "confidence": confidence,
        "value_flag": "",  # можно позже добавить
        "actual_winner": match.get("actual_winner", "")
    }

    predictions.append(record)
    logging.info(f"🤖 {record['team_a']} vs {record['team_b']} → предсказано: {predicted} (уверенность: {confidence})")

# Сохраняем
os.makedirs(os.path.dirname(PREDICTIONS_LOG_PATH), exist_ok=True)

if os.path.exists(PREDICTIONS_LOG_PATH):
    df_old = pd.read_csv(PREDICTIONS_LOG_PATH)
    df_new = pd.DataFrame(predictions)
    df_full = pd.concat([df_new, df_old], ignore_index=True)
else:
    df_full = pd.DataFrame(predictions)

# Удаляем дубли по match_id (последнее предсказание приоритетнее)
df_full.drop_duplicates(subset=['match_id'], keep='first', inplace=True)
field_order = [
    "timestamp", "match_id", "team_a", "team_b",
    "team_a_heroes", "team_b_heroes",
    "predicted_winner", "confidence", "value_flag", "actual_winner"
]
df_full = df_full[field_order] if all(col in df_full.columns for col in field_order) else df_full
df_full.to_csv(PREDICTIONS_LOG_PATH, index=False, encoding='utf-8')

logging.info(f"✅ Прогнозы сохранены: {len(predictions)} новых записей в {PREDICTIONS_LOG_PATH}")
