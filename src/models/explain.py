from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd

import shap


def _get_feature_names(bundle: Dict[str, Any]) -> List[str]:
    pipeline = bundle["pipeline"]
    try:
        names = pipeline.named_steps["preprocess"].get_feature_names_out()
        return names.tolist()
    except Exception:
        return [f"f{i}" for i in range(pipeline.named_steps["preprocess"].transform(pd.DataFrame([{}])).shape[1])]


def shap_explain_instance(bundle: Dict[str, Any], X: pd.DataFrame, top_k: int = 10) -> Dict[str, Any]:
    pipeline = bundle["pipeline"]

    # Build a prediction function over the transformed features
    def predict_proba_fn(df: pd.DataFrame) -> np.ndarray:
        return pipeline.predict_proba(df)[:, 1]

    # Use SHAP Explainer (model-agnostic) on the pipeline directly
    explainer = shap.Explainer(predict_proba_fn, X)
    shap_values = explainer(X.iloc[[0]])

    feature_names = X.columns.tolist()
    values = shap_values.values[0]
    abs_order = np.argsort(np.abs(values))[::-1]
    top_idx = abs_order[:top_k]

    contributions = [
        {"feature": feature_names[i], "shap_value": float(values[i])}
        for i in top_idx
    ]

    return {
        "contributions": contributions,
        "expected_value": float(np.ravel(shap_values.base_values)[0]) if hasattr(shap_values, "base_values") else None,
    }


