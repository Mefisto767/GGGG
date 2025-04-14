import os
import json
from ml.draft_analyzer import evaluate_draft

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_DIR = os.path.join(BASE_DIR, 'data_collector')

POWER_PATH = os.path.join(JSON_DIR, 'hero_power.json')
SYNERGY_PATH = os.path.join(JSON_DIR, 'hero_synergy.json')

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def calculate_draft_ratings(team_a_heroes, team_b_heroes):
    hero_power = load_json(POWER_PATH)
    hero_synergy = load_json(SYNERGY_PATH)

    a_scores = evaluate_draft(team_a_heroes, hero_power, hero_synergy)
    b_scores = evaluate_draft(team_b_heroes, hero_power, hero_synergy)

    total_a = a_scores['power'] + a_scores['synergy']
    total_b = b_scores['power'] + b_scores['synergy']

    return {
        'team_a': {**a_scores, 'total': total_a},
        'team_b': {**b_scores, 'total': total_b},
        'diff': total_a - total_b
    }

if __name__ == '__main__':
    sample_a = [1, 2, 3, 4, 5]
    sample_b = [6, 7, 8, 9, 10]
    result = calculate_draft_ratings(sample_a, sample_b)
    print(json.dumps(result, indent=2))
