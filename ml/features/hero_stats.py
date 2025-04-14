# ml/features/hero_stats.py

import numpy as np

def get_team_power(hero_ids: list[int], hero_power_dict: dict[int, float]) -> float:
    """
    Возвращает среднюю силу команды на основе hero_ids.
    """
    if not hero_ids:
        return 0.0
    values = [hero_power_dict.get(h, 0) for h in hero_ids]
    return float(np.mean(values)) if values else 0.0


def get_team_synergy(hero_ids: list[int], synergy_matrix: dict[tuple[int, int], float]) -> float:
    """
    Возвращает синергию команды: среднее значение всех парных взаимодействий между героями.
    """
    if not hero_ids or len(hero_ids) < 2:
        return 0.0
    synergy_scores = []
    for i in range(len(hero_ids)):
        for j in range(i + 1, len(hero_ids)):
            pair = (hero_ids[i], hero_ids[j])
            reversed_pair = (hero_ids[j], hero_ids[i])
            synergy = synergy_matrix.get(pair) or synergy_matrix.get(reversed_pair)
            if synergy is not None:
                synergy_scores.append(synergy)
    return float(np.mean(synergy_scores)) if synergy_scores else 0.0
