import pandas as pd

df = pd.read_csv('../logs/match_log.csv')
print("Всего строк:", len(df))
print("Колонки:", df.columns)
print("\nУникальные значения actual_winner:")
print(df['actual_winner'].value_counts())

print("\nПример строк, где actual_winner не входит в team_a / team_b:")
bad = df[~df['actual_winner'].isin(df['team_a']) & ~df['actual_winner'].isin(df['team_b'])]
print(bad[['team_a', 'team_b', 'actual_winner']].head(10))
