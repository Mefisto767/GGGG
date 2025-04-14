# ml/features/calculate_team_stats.py

import os
import json
from statistics import mean
import pandas as pd

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
HERO_POWER_PATH = os.path.join(PROJECT_DIR, "data_collector", "hero_power.json")

def load_hero_power():
    with open(HERO_POWER_PATH, "r", encoding="utf-8") as f:
        raw = json.load(f)
        try:
            return {int(k): float(v) for k, v in raw.items()}
        except:
            return {}

def calculate_team_stats(df: pd.DataFrame) -> pd.DataFrame:
    hero_power = load_hero_power()

    def avg_power(hero_list):
        if not isinstance(hero_list, list) or not hero_list:
            return 0.5
        powers = [hero_power.get(int(h), 0.5) for h in hero_list]
        return mean(powers) if powers else 0.5

    df["team_a_power"] = df["team_a_heroes"].apply(avg_power)
    df["team_b_power"] = df["team_b_heroes"].apply(avg_power)

    return df
