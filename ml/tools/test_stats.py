import pandas as pd
from ml.features.calculate_team_stats import calculate_team_stats

df = pd.DataFrame([{
    'team_a_form': ['W', 'W', 'L'],
    'team_b_form': ['L', 'L', 'W'],
    'team_a_winrate': 0.6,
    'team_b_winrate': 0.3,
    'team_a_picks': ['Invoker', 'Pudge'],
    'team_b_picks': ['Drow Ranger', 'Crystal Maiden']
}])

df = calculate_team_stats(df)
print(df.head())
