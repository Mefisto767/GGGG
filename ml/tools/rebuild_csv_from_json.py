import os
import json
import pandas as pd
import logging

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
NEW_MATCHES_JSON = os.path.join(BASE_DIR, 'data_collector', 'new_matches.json')
NEW_MATCHES_CSV = os.path.join(BASE_DIR, 'logs', 'new_matches.csv')

print("➡️ NEW_MATCHES_JSON path:", NEW_MATCHES_JSON)
print("➡️ Существует ли файл?", os.path.exists(NEW_MATCHES_JSON))

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def rebuild_from_json():
    if not os.path.exists(NEW_MATCHES_JSON):
        logger.warning("❌ Файл new_matches.json не найден.")
        return False

    with open(NEW_MATCHES_JSON, 'r', encoding='utf-8') as f:
        try:
            matches = json.load(f)
        except json.JSONDecodeError:
            logger.error("❌ Ошибка чтения JSON.")
            return False

    if not matches:
        logger.info("ℹ️ Нет данных в new_matches.json.")
        return False

    df = pd.DataFrame([{
        'team_a': m['radiant_team'],
        'team_b': m['dire_team'],
        'actual_winner': m['radiant_team'] if m['actual_winner'] == 'Radiant' else m['dire_team']
    } for m in matches])

    os.makedirs(os.path.dirname(NEW_MATCHES_CSV), exist_ok=True)
    df.to_csv(NEW_MATCHES_CSV, index=False, encoding='utf-8')
    logger.info(f"✅ CSV сохранён: {NEW_MATCHES_CSV} ({len(df)} матчей)")

    # Очистка JSON
    with open(NEW_MATCHES_JSON, 'w', encoding='utf-8') as f:
        json.dump([], f)
        logger.info("🧹 new_matches.json очищен.")

    return True

if __name__ == "__main__":
    rebuild_from_json()