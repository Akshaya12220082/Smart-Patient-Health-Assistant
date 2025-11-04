"""
Training utilities for disease risk models.
Builds simple baseline pipelines and persists them.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Tuple, Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier

from src.utils import load_config, ensure_dir


TARGET_CANDIDATES = ["Outcome", "target", "classification", "class"]


def _detect_target_column(df: pd.DataFrame) -> str:
    for col in TARGET_CANDIDATES:
        if col in df.columns:
            return col
    # fallback: last column if binary-looking
    last = df.columns[-1]
    unique_vals = set(df[last].dropna().unique().tolist())
    if unique_vals.issubset({0, 1}) and len(unique_vals) <= 2:
        return last
    raise ValueError("Could not determine target column. Please include one of: " + ", ".join(TARGET_CANDIDATES))


def _split_features(df: pd.DataFrame, target_col: str) -> Tuple[pd.DataFrame, pd.Series]:
    X = df.drop(columns=[target_col]) if target_col in df.columns else df.copy()
    y = df[target_col] if target_col in df.columns else None
    return X, y


def _build_pipeline(X: pd.DataFrame) -> Pipeline:
    numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
    categorical_cols = X.select_dtypes(exclude=["number"]).columns.tolist()

    numeric_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_cols),
            ("cat", categorical_pipeline, categorical_cols),
        ],
        remainder="drop",
    )

    # Base learners
    lr = LogisticRegression(max_iter=1000, n_jobs=None)
    rf = RandomForestClassifier(n_estimators=300, random_state=42)
    # Optional XGBoost/LightGBM if installed
    estimators = [("lr", lr), ("rf", rf)]
    try:
        from xgboost import XGBClassifier  # type: ignore
        xgb = XGBClassifier(
            n_estimators=400,
            max_depth=4,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=42,
        )
        estimators.append(("xgb", xgb))
    except Exception:
        pass
    try:
        from lightgbm import LGBMClassifier  # type: ignore
        lgbm = LGBMClassifier(
            n_estimators=500,
            learning_rate=0.05,
            num_leaves=31,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42,
        )
        estimators.append(("lgbm", lgbm))
    except Exception:
        pass

    model = VotingClassifier(estimators=estimators, voting="soft")

    pipe = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("clf", model),
    ])
    return pipe


def _encode_target_series(y: pd.Series, condition: str) -> Tuple[pd.Series, Dict[Any, int]]:
    """
    Encode non-numeric binary targets to {0,1}. Tries to map disease-present labels to 1.
    """
    if y is None:
        raise ValueError("Target series y is None")

    if pd.api.types.is_numeric_dtype(y):
        unique = sorted(set(int(v) for v in pd.Series(y).dropna().unique().tolist()))
        if set(unique).issubset({0, 1}):
            mapping = {0: 0, 1: 1}
            return y.astype(int), mapping
        # Coerce to 0/1 if numeric but not 0/1
        y_bin = (pd.to_numeric(y, errors="coerce") > 0).astype(int)
        mapping = {0: 0, 1: 1}
        return y_bin, mapping

    # Object or categorical with two classes expected
    classes = [str(v).lower() for v in pd.Series(y).dropna().unique().tolist()]
    if len(classes) != 2:
        raise ValueError(f"Expected binary target, found classes: {classes}")

    positive_keywords = {"1", "yes", "true", "ckd", "present", "abnormal", "disease", "positive"}
    # Heuristic for condition-specific positive label
    if condition.lower() == "kidney":
        preferred_positive = "ckd"
    elif condition.lower() == "heart":
        preferred_positive = "1"
    elif condition.lower() == "diabetes":
        preferred_positive = "1"
    else:
        preferred_positive = None

    cls0, cls1 = classes[0], classes[1]
    def is_positive(label: str) -> bool:
        if preferred_positive and preferred_positive == label:
            return True
        return label in positive_keywords

    pos_label = cls1 if is_positive(cls1) else (cls0 if is_positive(cls0) else cls1)
    neg_label = cls0 if pos_label == cls1 else cls1

    mapping = {neg_label: 0, pos_label: 1}
    y_mapped = pd.Series([mapping[str(v).lower()] for v in y], index=y.index)
    return y_mapped.astype(int), mapping


@dataclass
class TrainResult:
    condition: str
    model_path: str
    metrics: Dict[str, float]


class ModelTrainer:
    def __init__(self, config_path: str | None = None) -> None:
        self.config = load_config(config_path)
        self.save_dir = self.config["models"]["save_dir"]
        ensure_dir(self.save_dir)

    def train_and_save(self, condition: str, df: pd.DataFrame) -> TrainResult:
        target_col = _detect_target_column(df)
        X, y = _split_features(df, target_col)
        y_encoded, label_mapping = _encode_target_series(y, condition)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded,
            test_size=self.config["models"].get("test_size", 0.2),
            random_state=self.config["models"].get("random_state", 42),
            stratify=y_encoded if y_encoded.nunique() <= 10 else None,
        )

        pipe = _build_pipeline(X)
        pipe.fit(X_train, y_train)

        y_prob = pipe.predict_proba(X_test)[:, 1]
        y_pred = (y_prob >= 0.5).astype(int)

        metrics = {
            "roc_auc": float(roc_auc_score(y_test, y_prob)),
            "accuracy": float(accuracy_score(y_test, y_pred)),
        }

        model_path = os.path.join(self.save_dir, f"{condition}_model.joblib")
        joblib.dump({
            "pipeline": pipe,
            "target_col": target_col,
            "feature_columns": X.columns.tolist(),
            "metrics": metrics,
            "label_mapping": label_mapping,
        }, model_path)

        return TrainResult(condition=condition, model_path=model_path, metrics=metrics)


def load_trained_model(condition: str, config_path: str | None = None) -> Dict[str, Any]:
    config = load_config(config_path)
    model_path = os.path.join(config["models"]["save_dir"], f"{condition}_model.joblib")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}. Train the model first.")
    return joblib.load(model_path)


