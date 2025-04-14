import csv
import os

def analyze_log():
    log_path = os.path.join(os.path.dirname(__file__), "../logs/match_log.csv")
    total = 0
    correct = 0
    value_bets = 0
    value_hits = 0
    profit = 0
    stake = 100  # Фиксированная ставка

    if not os.path.exists(log_path):
        print("❌ Файл журнала не найден.")
        return

    with open(log_path, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    if not rows:
        print("ℹ️ Файл пустой или нет данных.")
        return

    for row in rows:
        if not row.get("actual_winner") or not row.get("predicted_winner"):
            continue

        total += 1
        predicted = row["predicted_winner"].strip()
        actual = row["actual_winner"].strip()

        try:
            confidence = int(row["confidence"])
        except (ValueError, TypeError):
            confidence = 0

        is_value = row.get("value_flag", "").strip().lower() == "yes"

        if is_value:
            value_bets += 1
            if predicted == actual:
                value_hits += 1
                profit += stake * 1.8  # Примерный кэф
            else:
                profit -= stake
        else:
            if predicted == actual:
                correct += 1

    winrate = (correct / total * 100) if total else 0
    roi = (profit / (value_bets * stake) * 100) if value_bets else 0

    print("\n📊 Статистика:")
    print(f"Всего матчей с результатом: {total}")
    print(f"✅ Точных прогнозов (без value): {correct} ({winrate:.1f}%)")
    print(f"💸 Value-ставок: {value_bets}, Зашло: {value_hits}")
    print(f"📈 ROI на value: {roi:.2f}%")
    print(f"💰 Прибыль: {profit:.2f} руб.")

if __name__ == "__main__":
    analyze_log()