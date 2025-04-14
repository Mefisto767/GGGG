import os
import joblib
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(PROJECT_ROOT, 'ml', 'model.pkl')
ENCODER_PATH = os.path.join(PROJECT_ROOT, 'ml', 'onehot_encoder.pkl')
FEATURES_PATH = os.path.join(PROJECT_ROOT, 'ml', 'feature_names.pkl')
LOG_PATH = os.path.join(PROJECT_ROOT, 'logs', 'match_log.csv')

def make_predictions():
    df = pd.read_csv(LOG_PATH)
    df_pred = df[df['predicted_winner'].isna()].copy()

    if df_pred.empty:
        print("ℹ️ Нет новых матчей для предсказания.")
        return

    model = joblib.load(MODEL_PATH)
    encoder = joblib.load(ENCODER_PATH)
    expected_features = joblib.load(FEATURES_PATH)

    X_raw = df_pred[['team_a', 'team_b']]
    X_encoded = encoder.transform(X_raw)
    X_df = pd.DataFrame(X_encoded.toarray(), columns=encoder.get_feature_names_out(['team_a', 'team_b']))

    # Подгон под обучающую выборку (если что-то исчезло/добавилось)
    for col in expected_features:
        if col not in X_df:
            X_df[col] = 0
    X_df = X_df[expected_features]

    probs = model.predict_proba(X_df)
    preds = model.predict(X_df)
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
