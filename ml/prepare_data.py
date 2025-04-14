import os
import json
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

JSON_PATH = os.path.join(os.path.dirname(__file__), "..", "data_collector", "matches.json")
CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data_collector", "combined_matches.csv")

def load_and_prepare_data():
    df = pd.read_csv(CSV_PATH)

    df["team_a_heroes"] = df["team_a_heroes"].apply(lambda x: eval(x) if isinstance(x, str) else [])
    df["team_b_heroes"] = df["team_b_heroes"].apply(lambda x: eval(x) if isinstance(x, str) else [])

    df = df[
        df["team_a_heroes"].apply(lambda x: isinstance(x, list) and len(x) == 5) &
        df["team_b_heroes"].apply(lambda x: isinstance(x, list) and len(x) == 5)
    ]

    df = df.dropna(subset=["actual_winner"])
    df["label"] = df.apply(lambda row: 0 if row["actual_winner"] == row["team_a"] else 1, axis=1)

    X_raw = df[["team_a", "team_b", "team_a_heroes", "team_b_heroes"]].copy()
    X_features = X_raw.apply(lambda row: [
        row["team_a"],
        row["team_b"],
        *row["team_a_heroes"],
        *row["team_b_heroes"]
    ], axis=1).tolist()

    encoder = OneHotEncoder(handle_unknown="ignore", sparse=False)
    X_encoded = encoder.fit_transform(X_features)

    return X_encoded, df["label"].values, encoder

def encode_match(match: dict, encoder: OneHotEncoder) -> list:
    features = [
        match.get("team_a"),
        match.get("team_b"),
        *match.get("team_a_heroes", []),
        *match.get("team_b_heroes", [])
    ]
    return encoder.transform([features]).tolist()[0]