# analytics/predictor.py

import os
import joblib
import pandas as pd
import numpy as np
import ast

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, 'ml', 'model.pkl')
LOG_PATH = os.path.join(PROJECT_ROOT, 'logs', 'match_log.csv')

def safe_eval(value):
    try:
        return ast.literal_eval(value) if isinstance(value, str) else value
    except Exception:
        return []

def avg_power(heroes):
    return sum(heroes) / len(heroes) if isinstance(heroes, list) and len(heroes) == 5 else 0

def make_predictions():
    df = pd.read_csv(LOG_PATH)
    df_pred = df[df['predicted_winner'].isna()].copy()

    if df_pred.empty:
        print("ℹ️ Нет новых матчей для предсказания.")
        return

    model = joblib.load(MODEL_PATH)

    df_pred['team_a_heroes'] = df_pred['team_a_heroes'].apply(safe_eval)
    df_pred['team_b_heroes'] = df_pred['team_b_heroes'].apply(safe_eval)

    df_pred['team_a_power'] = df_pred['team_a_heroes'].apply(avg_power)
    df_pred['team_b_power'] = df_pred['team_b_heroes'].apply(avg_power)

    X = df_pred[['team_a_power', 'team_b_power']]
    probs = model.predict_proba(X)
    preds = model.predict(X)
    confidences = np.max(probs, axis=1)

    df.loc[df_pred.index, 'predicted_winner'] = preds
    df.loc[df_pred.index, 'confidence'] = confidences
    df.loc[df_pred.index, 'value_flag'] = (confidences > 0.7).astype(int)

    df.to_csv(LOG_PATH, index=False)

    for team_a, team_b, pred, conf in zip(df_pred['team_a'], df_pred['team_b'], preds, confidences):
        print(f"🤖 {team_a} vs {team_b} → предсказано: {pred} (уверенность: {conf:.2f})")

    print(f"✅ Предсказания завершены: {len(preds)} матчей.")

if __name__ == "__main__":
    make_predictions()
