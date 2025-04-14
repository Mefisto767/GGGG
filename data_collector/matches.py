import json
import os

def get_latest_match():
    path = os.path.join(os.path.dirname(__file__), "sample_match.json")
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data
