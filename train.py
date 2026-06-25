from pathlib import Path
import json

from joblib import dump
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def main() -> None:
    data = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        data.data,
        data.target,
        test_size=0.2,
        random_state=42,
        stratify=data.target,
    )

    model = LogisticRegression(max_iter=200)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)

    output_dir = Path("models")
    output_dir.mkdir(parents=True, exist_ok=True)

    dump(model, output_dir / "iris_model.joblib")
    with open(output_dir / "metrics.json", "w", encoding="utf-8") as f:
        json.dump({"accuracy": accuracy}, f, indent=2)

    print(f"Training finished. Accuracy: {accuracy:.4f}")


if __name__ == "__main__":
    main()
