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
    except Exception:
        return []


def load_and_prepare_data(path):
    df = pd.read_csv(path)
    print(f"🔍 Все строки: {len(df)}")

    team_a_col, team_b_col = "team_a", "team_b"
    heroes_a_col, heroes_b_col = "team_a_heroes", "team_b_heroes"

    df[heroes_a_col] = df[heroes_a_col].apply(safe_eval)
    df[heroes_b_col] = df[heroes_b_col].apply(safe_eval)

    df = df[df[heroes_a_col].apply(lambda x: isinstance(x, list) and len(x) == 5)]
    df = df[df[heroes_b_col].apply(lambda x: isinstance(x, list) and len(x) == 5)]
    print(f"✅ Строк с валидными героями: {len(df)}")

    df = df.dropna(subset=["actual_winner"])
    print(f"✅ После dropna: {len(df)}")

    df = df[df["actual_winner"].isin(df[team_a_col]) | df["actual_winner"].isin(df[team_b_col])]
    print(f"✅ Победитель входит в команду: {len(df)}")

    if len(df) == 0:
        return None, None, None, None, df, heroes_a_col, heroes_b_col

    X_cats = df[[team_a_col, team_b_col]]
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X_cats)
    feature_names = encoder.get_feature_names_out([team_a_col, team_b_col])

    extra_features = df[["team_a_power", "team_b_power", "team_a_synergy", "team_b_synergy"]].fillna(0)
    X_final = np.hstack([X_encoded.toarray(), extra_features.to_numpy()])
    y = df["actual_winner"]

    return X_final, y, encoder, feature_names, df, heroes_a_col, heroes_b_col


def train_model(csv_path=None):
    print("📦 Загрузка и подготовка данных...")
    csv_path = csv_path or CSV_PATH
    X, y, encoder, feature_names, df, ha, hb = load_and_prepare_data(csv_path)

    if X is None or len(y) == 0:
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
    print(f"Команд-победителей: {sum(y == df['team_a']) + sum(y == df['team_b'])}")
    print(f"Мин. уверенность (на обучении): {np.min(model.predict_proba(X).max(axis=1)):.2f}")
    print(f"Средняя мощь команд: A={df[ha].apply(lambda x: np.mean(x)).mean():.1f}, "
          f"B={df[hb].apply(lambda x: np.mean(x)).mean():.1f}")


if __name__ == "__main__":
    train_model()
