import os
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
import ast

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(PROJECT_ROOT, 'data_collector', 'combined_matches.csv')
MODEL_PATH = os.path.join(PROJECT_ROOT, 'ml', 'model.pkl')
ENCODER_PATH = os.path.join(PROJECT_ROOT, 'ml', 'onehot_encoder.pkl')
FEATURES_PATH = os.path.join(PROJECT_ROOT, 'ml', 'feature_names.pkl')

def safe_eval(val):
    try:
        return ast.literal_eval(val) if isinstance(val, str) else val
    except:
        return []

def find_column(possible_names, df):
    for name in possible_names:
        if name in df.columns:
            return name
    return None

def load_and_prepare_data(path):
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    df = df.dropna(subset=["actual_winner"])

    team_a_col = find_column(["team_a", "team_a_x", "team_a_y"], df)
    team_b_col = find_column(["team_b", "team_b_x", "team_b_y"], df)
    heroes_a_col = find_column(["team_a_heroes", "team_a_heroes_x", "team_a_heroes_y"], df)
    heroes_b_col = find_column(["team_b_heroes", "team_b_heroes_x", "team_b_heroes_y"], df)

    print(f"🔎 team_a_col: {team_a_col}, team_b_col: {team_b_col}")
    print(f"🔎 heroes_a_col: {heroes_a_col}, heroes_b_col: {heroes_b_col}")

    if not all([team_a_col, team_b_col, heroes_a_col, heroes_b_col]):
        raise ValueError("❌ Не найдены нужные колонки!")

    df[heroes_a_col] = df[heroes_a_col].apply(safe_eval)
    df[heroes_b_col] = df[heroes_b_col].apply(safe_eval)

    df = df[df[team_a_col].notna() & df[team_b_col].notna()]
    df = df[df["actual_winner"].isin(df[team_a_col]) | df["actual_winner"].isin(df[team_b_col])]
    df = df[df[heroes_a_col].apply(lambda x: isinstance(x, list) and len(x) == 5)]
    df = df[df[heroes_b_col].apply(lambda x: isinstance(x, list) and len(x) == 5)]

    X = df[[team_a_col, team_b_col]]
    y = df["actual_winner"]

    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X)
    feature_names = encoder.get_feature_names_out([team_a_col, team_b_col])

    return X_encoded, y, encoder, feature_names, df, heroes_a_col, heroes_b_col

def train_model(csv_path=None):
    print("📦 Загрузка и подготовка данных...")
    csv_path = csv_path or CSV_PATH

    X, y, encoder, feature_names, df, heroes_a_col, heroes_b_col = load_and_prepare_data(csv_path)

    if X.shape[0] == 0 or len(y) == 0:
        print("❌ Недостаточно данных для обучения.")
        return

    print(f"📊 Обучение на {X.shape[0]} матчах.")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)
    joblib.dump(list(feature_names), FEATURES_PATH)

    print(f"✅ Модель обучена и сохранена: {MODEL_PATH}")
    print(f"Всего матчей в обучении: {len(df)}")
    print(f"Команд-победителей: {sum(y == df.iloc[:, df.columns.get_loc('actual_winner')])}")
    print(f"Мин. уверенность: {np.min(model.predict_proba(X).max(axis=1)):.2f}")
    print(f"Средняя мощь: A={df[heroes_a_col].apply(lambda x: np.mean(x)).mean():.1f}, "
          f"B={df[heroes_b_col].apply(lambda x: np.mean(x)).mean():.1f}")

if __name__ == "__main__":
    train_model()
