import csv
import os
import requests

def get_actual_winner(match_id):
    try:
        url = f"https://api.opendota.com/api/matches/{match_id}"
        response = requests.get(url)
        data = response.json()

        radiant_win = data.get("radiant_win")
        radiant_name = data.get("radiant_name", "Radiant")
        dire_name = data.get("dire_name", "Dire")

        return radiant_name if radiant_win else dire_name
    except Exception as e:
        print(f"[Ошибка получения результата матча {match_id}]: {e}")
        return None

def update_match_log():
    path = os.path.join(os.path.dirname(__file__), "../logs/match_log.csv")
    if not os.path.exists(path):
        print("❌ Файл match_log.csv не найден.")
        return

    updated_rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for row in rows:
        if row.get("actual_winner") and row["actual_winner"].strip():
            updated_rows.append(row)
            continue

        match_id = row["match_id"]
        actual_winner = get_actual_winner(match_id)
        if actual_winner:
            print(f"✅ Получен победитель для матча {match_id}: {actual_winner}")
            row["actual_winner"] = actual_winner
        else:
            print(f"⚠️ Не удалось получить результат для матча {match_id}")

        updated_rows.append(row)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(updated_rows)

if __name__ == "__main__":
    update_match_log()
