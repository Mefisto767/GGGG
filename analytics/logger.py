import csv
import os
from datetime import datetime


def log_match_result(match, prediction, value_flag):
    log_path = os.path.join(os.path.dirname(__file__), "../logs/match_log.csv")

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "match_id": match["match_id"],
        "team_a": match["team_a"],
        "team_b": match["team_b"],
        "predicted_winner": prediction["winner"],
        "confidence": prediction["confidence"],
        "value_flag": "yes" if value_flag else "no",
        "actual_winner": ""  # Пока вручную, потом можно автоматизировать
    }

    file_exists = os.path.isfile(log_path)
    with open(log_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=row.keys())
        if not file_exists or os.stat(log_path).st_size == 0:
            writer.writeheader()
        writer.writerow(row)

