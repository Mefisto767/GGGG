# ml/tools/convert_hero_json_to_pkl.py

import os
import json
import joblib

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS_DIR = os.path.join(PROJECT_ROOT, "ml", "tools")
DATA_DIR = os.path.join(PROJECT_ROOT, "ml", "data")

# Создаём папку data, если её нет
os.makedirs(DATA_DIR, exist_ok=True)

def convert_json_to_pkl(json_filename, pkl_filename):
    json_path = os.path.join(TOOLS_DIR, json_filename)
    pkl_path = os.path.join(DATA_DIR, pkl_filename)

    print(f"📥 Загрузка {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"💾 Сохранение в {pkl_path}")
    joblib.dump(data, pkl_path)
    print("✅ Готово.")

def main():
    convert_json_to_pkl("hero_power.json", "hero_power.pkl")
    convert_json_to_pkl("hero_synergy.json", "hero_synergy.pkl")

if __name__ == "__main__":
    main()
