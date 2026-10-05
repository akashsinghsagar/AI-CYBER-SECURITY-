"""End-to-end AI cyber threat awareness and detection prototype.

The script performs EDA, preprocessing, supervised classification, a small
MLP-based deep-learning prototype, evaluation, and optional test prediction.
It is intentionally reproducible and keeps all learned transformations inside
scikit-learn pipelines to avoid data leakage.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RANDOM_STATE = 42
TARGET = "class"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train", type=Path, default=None)
    parser.add_argument("--test", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    return parser.parse_args()


def locate_file(name: str, explicit: Path | None, project_root: Path) -> Path:
    candidates = [explicit] if explicit else [
        project_root / "data" / name,
        project_root / name,
    ]
    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    searched = ", ".join(str(path) for path in candidates if path)
    raise FileNotFoundError(f"Could not find {name}. Searched: {searched}")


def make_preprocessor(features: pd.DataFrame) -> ColumnTransformer:
    categorical = features.select_dtypes(include=["object", "category"]).columns.tolist()
    numeric = features.select_dtypes(exclude=["object", "category"]).columns.tolist()
    numeric_pipe = Pipeline(
        [("imputer", SimpleImputer(strategy="median")), ("scaler", StandardScaler())]
    )
    categorical_pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        [("numeric", numeric_pipe, numeric), ("categorical", categorical_pipe, categorical)],
        remainder="drop",
    )


def build_models(features: pd.DataFrame) -> dict[str, Pipeline]:
    return {
        "logistic_regression": Pipeline(
            [
                ("preprocess", make_preprocessor(features)),
                ("model", LogisticRegression(max_iter=300, random_state=RANDOM_STATE)),
            ]
        ),
        "mlp_neural_network": Pipeline(
            [
                ("preprocess", make_preprocessor(features)),
                (
                    "model",
                    MLPClassifier(
                        hidden_layer_sizes=(32, 16),
                        max_iter=50,
                        # sklearn's early-stopping scorer currently applies
                        # np.isnan to string predictions in this environment.
                        early_stopping=False,
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        ),
    }


def save_eda_plots(train: pd.DataFrame, output_dir: Path) -> None:
    sns.set_theme(style="whitegrid")
    counts = train[TARGET].value_counts().rename(index={"normal": "Normal", "anomaly": "Suspicious"})
    ax = counts.plot(kind="bar", color=["#2a9d8f", "#e76f51"], figsize=(7, 4))
    ax.set_title("Normal vs suspicious network events")
    ax.set_xlabel("Event class")
    ax.set_ylabel("Number of events")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(output_dir / "class_distribution.png", dpi=150)
    plt.close()

    plot_features = ["src_bytes", "dst_bytes", "count", "serror_rate"]
    available = [column for column in plot_features if column in train.columns]
    melted = train[available + [TARGET]].melt(id_vars=TARGET, var_name="feature", value_name="value")
    chart = sns.boxplot(data=melted, x="feature", y="value", hue=TARGET, showfliers=False)
    chart.set_title("Distribution of selected attack-related features")
    chart.tick_params(axis="x", rotation=25)
    plt.tight_layout()
    plt.savefig(output_dir / "feature_distributions.png", dpi=150)
    plt.close()

    suspicious = train[TARGET].eq("anomaly")
    indicator_columns = [
        column for column in ["num_failed_logins", "num_compromised", "root_shell", "su_attempted"]
        if column in train.columns
    ]
    indicator_rates = train.loc[suspicious, indicator_columns].gt(0).mean().sort_values(ascending=False)
    indicator_rates.plot(kind="bar", color="#f4a261", figsize=(7, 4))
    plt.title("Suspicious events containing threat indicators")
    plt.ylabel("Fraction of suspicious events")
    plt.xlabel("Indicator")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(output_dir / "threat_indicators.png", dpi=150)
    plt.close()


def evaluate_model(
    name: str, model: Pipeline, x_train: pd.DataFrame, x_valid: pd.DataFrame,
    y_train: pd.Series, y_valid: pd.Series,
) -> dict[str, float | str]:
    started = time.perf_counter()
    model.fit(x_train, y_train)
    elapsed = time.perf_counter() - started
    predictions = model.predict(x_valid)
    return {
        "model": name,
        "accuracy": accuracy_score(y_valid, predictions),
        "precision": precision_score(y_valid, predictions, pos_label="anomaly", zero_division=0),
        "recall": recall_score(y_valid, predictions, pos_label="anomaly", zero_division=0),
        "f1_score": f1_score(y_valid, predictions, pos_label="anomaly", zero_division=0),
        "training_time_seconds": elapsed,
        "classification_report": classification_report(y_valid, predictions, zero_division=0),
        "confusion_matrix": confusion_matrix(y_valid, predictions, labels=["normal", "anomaly"]).tolist(),
    }


def main() -> None:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    output_dir = args.output_dir if args.output_dir.is_absolute() else project_root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    train_path = locate_file("Train_data.csv", args.train, project_root)
    test_path = locate_file("Test_data.csv", args.test, project_root)

    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    if TARGET not in train:
        raise ValueError(f"Training data must contain a '{TARGET}' column.")
    x = train.drop(columns=TARGET)
    y = train[TARGET].astype(str).str.strip().str.lower()
    x_train, x_valid, y_train, y_valid = train_test_split(
        x, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    save_eda_plots(train, output_dir)
    results: list[dict[str, float | str]] = []
    models = build_models(x)
    for name, model in models.items():
        results.append(evaluate_model(name, model, x_train, x_valid, y_train, y_valid))
        model.fit(x, y)

    metrics = pd.DataFrame(
        [{key: value for key, value in result.items() if key not in {"classification_report", "confusion_matrix"}}
         for result in results]
    )
    metrics.to_csv(output_dir / "model_metrics.csv", index=False)
    (output_dir / "detailed_metrics.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    # Test_data.csv has no labels, so predictions are exported for analyst review.
    for name, model in models.items():
        predictions = model.predict(test)
        pd.DataFrame({"prediction": predictions}).to_csv(
            output_dir / f"{name}_test_predictions.csv", index=False
        )
    print(metrics.to_string(index=False))
    print(f"\nArtifacts written to: {output_dir}")


if __name__ == "__main__":
    main()
