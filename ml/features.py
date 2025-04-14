import pandas as pd
from collections import defaultdict


def calculate_team_stats(df: pd.DataFrame, form_window: int = 5) -> pd.DataFrame:
    """
    Добавляет признаки формы и винрейта команд на основе истории матчей
    """
    df = df.copy()

    # Словари для подсчета
    match_history = defaultdict(list)  # ключ: team -> list of results (1-win, 0-lose)
    total_matches = defaultdict(int)
    total_wins = defaultdict(int)

    form_team_a = []
    form_team_b = []
    winrate_team_a = []
    winrate_team_b = []

    for _, row in df.iterrows():
        a, b, winner = row['team_a'], row['team_b'], row['actual_winner']

        # Форма: последние N игр
        def recent_form(team):
            recent = match_history[team][-form_window:]
            return sum(recent) / len(recent) if recent else 0.5  # 0.5 если нет истории

        # Winrate: общее
        def win_rate(team):
            return total_wins[team] / total_matches[team] if total_matches[team] > 0 else 0.5

        form_team_a.append(recent_form(a))
        form_team_b.append(recent_form(b))

        winrate_team_a.append(win_rate(a))
        winrate_team_b.append(win_rate(b))

        # Обновляем статистику
        total_matches[a] += 1
        total_matches[b] += 1

        if winner == a:
            match_history[a].append(1)
            match_history[b].append(0)
            total_wins[a] += 1
        elif winner == b:
            match_history[a].append(0)
            match_history[b].append(1)
            total_wins[b] += 1

    df['form_team_a'] = form_team_a
    df['form_team_b'] = form_team_b
    df['winrate_team_a'] = winrate_team_a
    df['winrate_team_b'] = winrate_team_b

    return df
