# ml/train_model.py

import os
import pandas as pd
import joblib
import ast
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(PROJECT_ROOT, "data_collector", "combined_matches.csv")
MODEL_PATH = os.path.join(PROJECT_ROOT, "ml", "model.pkl")
ENCODER_PATH = os.path.join(PROJECT_ROOT, "ml", "label_encoder.pkl")

def safe_eval(value):
    try:
        return ast.literal_eval(value) if isinstance(value, str) else value
    except Exception:
        return []

def avg_power(heroes):
    return sum(heroes) / len(heroes) if isinstance(heroes, list) and len(heroes) == 5 else 0

def load_and_prepare_data():
    print("📦 Загрузка и подготовка данных...")
    df = pd.read_csv(CSV_PATH)

    df["team_a_heroes"] = df["team_a_heroes"].apply(safe_eval)
    df["team_b_heroes"] = df["team_b_heroes"].apply(safe_eval)

    df = df[
        df["team_a_heroes"].apply(lambda x: isinstance(x, list) and len(x) == 5) &
        df["team_b_heroes"].apply(lambda x: isinstance(x, list) and len(x) == 5)
    ]

    df["team_a_power"] = df["team_a_heroes"].apply(avg_power)
    df["team_b_power"] = df["team_b_heroes"].apply(avg_power)

    df.dropna(subset=["actual_winner"], inplace=True)

    encoder = LabelEncoder()
    df["label"] = encoder.fit_transform(df["actual_winner"])

    X = df[["team_a_power", "team_b_power"]]
    y = df["label"]

    return X, y, encoder, df

def train_model():
    X, y, encoder, df = load_and_prepare_data()

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)

    print("✅ Модель обучена и сохранена:", MODEL_PATH)

    print("\n📊 Статистика обучения:")
    print(f"Всего матчей в обучении: {len(df)}")
    print(f"Команд-победителей: {df['actual_winner'].nunique()}")
    print(f"Мин. уверенность (на обучении): {model.predict_proba(X).max(axis=1).min():.2f}")
    print(f"Средняя мощь команд: A={df['team_a_power'].mean():.1f}, B={df['team_b_power'].mean():.1f}")

if __name__ == "__main__":
    train_model()
