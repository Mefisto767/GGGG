import json
import os

def load_hero_meta():
    path = os.path.join(os.path.dirname(__file__), '../../data_collector/hero_power.json')
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

HERO_META = load_hero_meta()
