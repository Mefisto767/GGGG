def calculate_team_power(team, hero_power):
    """
    Подсчет силы команды на основе hero_power.
    :param team: список имен героев
    :param hero_power: словарь {hero_name: score}
    :return: суммарная сила команды
    """
    return sum(hero_power.get(hero, 0.5) for hero in team)  # 0.5 — дефолт, если героя нет в json
