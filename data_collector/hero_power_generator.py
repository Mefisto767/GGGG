import json
import os

# Путь до файла с мета-данными героев (который ты уже обновляешь)
META_PATH = "data_collector/hero_meta.json"
OUTPUT_PATH = "data_collector/hero_power.json"

def generate_hero_power():
    if not os.path.exists(META_PATH):
        print("⚠️ Файл hero_meta.json не найден.")
        return

    with open(META_PATH, encoding="utf-8") as f:
        hero_meta = json.load(f)

    power_data = {}
    for hero in hero_meta:
        name = hero["localized_name"]
        # Здесь можно поставить логику по ролям или статистике, пока дефолт
        power_data[name] = 50

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(power_data, f, ensure_ascii=False, indent=2)

    print(f"✅ Сила героев сохранена в {OUTPUT_PATH}. Героев: {len(power_data)}")

if __name__ == "__main__":
    generate_hero_power()
