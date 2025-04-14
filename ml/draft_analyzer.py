# draft_analyzer.py
import json
import os
import numpy as np
from collections import defaultdict

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SYNERGY_PATH = os.path.join(PROJECT_ROOT, 'data_collector', 'hero_synergy.json')
POWER_PATH = os.path.join(PROJECT_ROOT, 'data_collector', 'hero_power.json')


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def avg_power(heroes, hero_power):
    return np.mean([hero_power.get(str(h), 0.0) for h in heroes])


def team_synergy(heroes, synergy_map):
    scores = []
    for i in range(len(heroes)):
        for j in range(i + 1, len(heroes)):
            h1, h2 = str(heroes[i]), str(heroes[j])
            score = synergy_map.get(h1, {}).get(h2, 0.0)
            scores.append(score)
    return np.mean(scores) if scores else 0.0


def analyze_draft(radiant_heroes, dire_heroes):
    synergy_map = load_json(SYNERGY_PATH)
    hero_power = load_json(POWER_PATH)

    radiant = {
        'heroes': radiant_heroes,
        'avg_power': avg_power(radiant_heroes, hero_power),
        'synergy': team_synergy(radiant_heroes, synergy_map),
    }

    dire = {
        'heroes': dire_heroes,
        'avg_power': avg_power(dire_heroes, hero_power),
        'synergy': team_synergy(dire_heroes, synergy_map),
    }

    radiant['total_score'] = radiant['avg_power'] * 0.6 + radiant['synergy'] * 0.4
    dire['total_score'] = dire['avg_power'] * 0.6 + dire['synergy'] * 0.4

    result = {
        'radiant': radiant,
        'dire': dire,
        'winner': 'radiant' if radiant['total_score'] > dire['total_score'] else 'dire'
    }
    return result


if __name__ == "__main__":
    radiant_ids = [6, 26, 68, 96, 107]  # Пример
    dire_ids = [29, 30, 46, 71, 102]

    result = analyze_draft(radiant_ids, dire_ids)
    print("\n=== DRAFT ANALYSIS ===")
    print(f"Radiant Avg Power: {result['radiant']['avg_power']:.2f}, Synergy: {result['radiant']['synergy']:.2f}")
    print(f"Dire    Avg Power: {result['dire']['avg_power']:.2f}, Synergy: {result['dire']['synergy']:.2f}")
    print(f"➡️ Побеждает: {result['winner'].capitalize()}\n")
