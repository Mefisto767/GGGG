import os
import json
import numpy as np
from typing import List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data_collector')

WINRATE_FILE = os.path.join(DATA_DIR, 'hero_winrates.json')
SYNERGY_FILE = os.path.join(DATA_DIR, 'hero_synergy_matrix.json')


def get_team_power(team_heroes: List[int]) -> float:
    if not team_heroes:
        return 0.0
    try:
        with open(WINRATE_FILE, 'r', encoding='utf-8') as f:
            winrates = json.load(f)
        rates = [winrates.get(str(h), 0.5) for h in team_heroes]
        return float(np.mean(rates)) if rates else 0.0
    except Exception as e:
        print(f"[get_team_power] ⚠️ Ошибка: {e}")
        return 0.0


def get_team_synergy(team_heroes: List[int]) -> float:
    if not team_heroes or len(team_heroes) < 2:
        return 0.0
    try:
        with open(SYNERGY_FILE, 'r', encoding='utf-8') as f:
            synergy_matrix = json.load(f)

        synergies = []
        for i in range(len(team_heroes)):
            for j in range(i + 1, len(team_heroes)):
                h1, h2 = str(team_heroes[i]), str(team_heroes[j])
                score = synergy_matrix.get(h1, {}).get(h2, 0.0)
                synergies.append(score)

        return float(np.mean(synergies)) if synergies else 0.0
    except Exception as e:
        print(f"[get_team_synergy] ⚠️ Ошибка: {e}")
        return 0.0
