import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pickle
from ml.dataset_builder import build_dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def auto_train(threshold=20):
    X, y = build_dataset()

    if len(X) < threshold:
        print(f"⏳ Недостаточно данных для автообучения ({len(X)}/{threshold})")
        return False

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)

    acc = accuracy_score(y_test, model.predict(X_test))
    print(f"🤖 Автообучение завершено. Точность: {acc * 100:.2f}%")

    model_path = os.path.join(os.path.dirname(__file__), "model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print("📦 Обновлённая модель сохранена.")
    return True

if __name__ == "__main__":
    auto_train()
