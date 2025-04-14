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
    print(f"📦 Загрузка и подготовка данных...")
    print(f"🔍 Все строки: {len(df)}")

    # Создание финального столбца победителя
    df["actual_winner"] = df["actual_winner_x"].combine_first(df["actual_winner_y"])

    # Преобразование строк в списки героев
    df["team_a_heroes"] = df["team_a_heroes"].apply(safe_eval)
    df["team_b_heroes"] = df["team_b_heroes"].apply(safe_eval)

    # Фильтрация по героям
    df = df[df["team_a_heroes"].apply(lambda x: isinstance(x, list) and len(x) == 5)]
    df = df[df["team_b_heroes"].apply(lambda x: isinstance(x, list) and len(x) == 5)]
    print(f"✅ Строк с валидными героями: {len(df)}")

    # Удаление строк с пропущенными значениями
    df = df.dropna(subset=["team_a", "team_b", "actual_winner"])
    print(f"✅ После dropna: {len(df)}")

    # Проверка, что победитель входит в одну из команд
    df = df[df.apply(lambda row: row["actual_winner"] in [row["team_a"], row["team_b"]], axis=1)]
    print(f"✅ Победитель входит в команду: {len(df)}")

    if len(df) == 0:
        print("❌ Недостаточно данных для обучения.")
        return None, None, None, None, df, None, None

    X = df[["team_a", "team_b"]]
    y = df["actual_winner"]

    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X)
    feature_names = encoder.get_feature_names_out(["team_a", "team_b"])

    return X_encoded, y, encoder, feature_names, df, "team_a_heroes", "team_b_heroes"


def train_model(csv_path=None):
    csv_path = csv_path or CSV_PATH
    X, y, encoder, feature_names, df, heroes_a_col, heroes_b_col = load_and_prepare_data(csv_path)

    if X is None or X.shape[0] == 0 or len(y) == 0:
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
    print(f"Средняя мощь команд: A={df[heroes_a_col].apply(lambda x: np.mean(x) if x else 0).mean():.1f}, "
          f"B={df[heroes_b_col].apply(lambda x: np.mean(x) if x else 0).mean():.1f}")


if __name__ == "__main__":
    train_model()
