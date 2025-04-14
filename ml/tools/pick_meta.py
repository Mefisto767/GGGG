import os
import pandas as pd
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META_PATH = os.path.join(BASE_DIR, 'data_collector', 'hero_meta.csv')
NEW_JSON_PATH = os.path.join(BASE_DIR, 'data_collector', 'new_matches.json')

meta_df = pd.read_csv(META_PATH).set_index('hero_id')


def calculate_meta_score(picks):
    scores = [meta_df.loc[hid, 'win_rate'] for hid in picks if hid in meta_df.index]
    return sum(scores) / len(scores) if scores else 0.5


def enrich_matches_with_meta():
    if not os.path.exists(NEW_JSON_PATH):
        print("❌ new_matches.json не найден.")
        return

    with open(NEW_JSON_PATH, encoding='utf-8') as f:
        matches = json.load(f)

    for match in matches:
        match['meta_score_radiant'] = calculate_meta_score(match.get('radiant_picks', []))
        match['meta_score_dire'] = calculate_meta_score(match.get('dire_picks', []))

    with open(NEW_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(matches, f, indent=2, ensure_ascii=False)

    print(f"✅ Обновлено {len(matches)} матчей с мета-фичами.")


if __name__ == '__main__':
    enrich_matches_with_meta()
