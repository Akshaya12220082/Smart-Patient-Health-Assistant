"""
Simple rules-based recommendation engine with risk stratification.
"""

from __future__ import annotations

from typing import Dict, Any, List

from src.utils import load_config


def risk_band(score_0_100: float, config_path: str | None = None) -> str:
    """Determine risk band from score"""
    try:
        config = load_config(config_path)
        thresholds = config["risk_thresholds"]
        score = float(score_0_100)
        g0, g1 = thresholds["green"]
        y0, y1 = thresholds["yellow"]
        r0, r1 = thresholds["red"]
        if g0 <= score <= g1:
            return "green"
        if y0 <= score <= y1:
            return "yellow"
        if r0 <= score <= r1:
            return "red"
    except Exception:
        # Fallback to simple thresholds if config fails
        score = float(score_0_100)
        if score <= 30:
            return "green"
        elif score <= 70:
            return "yellow"
        else:
            return "red"
    return "unknown"


def _common_recos(band: str) -> List[str]:
    if band == "green":
        return [
            "Maintain a balanced diet rich in vegetables, fruits, and whole grains.",
            "Exercise at least 150 minutes per week (moderate intensity).",
            "Sleep 7-9 hours; keep a consistent schedule.",
            "Annual routine health check-up recommended.",
        ]
    if band == "yellow":
        return [
            "Schedule a consultation with a primary care physician within 2-4 weeks.",
            "Track BP, weight, and symptoms weekly.",
            "Moderate salt and sugar intake; avoid processed foods.",
            "Increase physical activity gradually with physician guidance.",
        ]
    if band == "red":
        return [
            "Seek medical attention promptly; consider ER if severe symptoms.",
            "Avoid strenuous activity until a doctor evaluates you.",
            "Keep emergency contacts and medical history ready.",
            "Monitor vitals closely; do not self-medicate.",
        ]
    return []


def _condition_specific(condition: str, band: str) -> List[str]:
    condition = condition.lower()
    if condition == "diabetes":
        if band == "green":
            return ["Prefer low-glycemic foods; routine fasting glucose every 6-12 months."]
        if band == "yellow":
            return ["Consider HbA1c test; dietician referral advisable."]
        if band == "red":
            return ["Urgent endocrinology review; check for hyper/hypoglycemia symptoms."]
    if condition == "heart":
        if band == "green":
            return ["Maintain BP <120/80; cardio exercise as tolerated."]
        if band == "yellow":
            return ["Consult cardiology; lipid profile and ECG suggested."]
        if band == "red":
            return ["Chest pain or dyspnea warrants immediate ER evaluation."]
    if condition == "kidney":
        if band == "green":
            return ["Hydration and moderate protein intake; annual eGFR."]
        if band == "yellow":
            return ["Nephrology consult; urine albumin/creatinine ratio test."]
        if band == "red":
            return ["Possible acute kidney risk—urgent labs and nephrology review."]
    return []


def generate_recommendations(condition: str, risk_score_0_100: float, config_path: str | None = None) -> Dict[str, Any]:
    band = risk_band(risk_score_0_100, config_path=config_path)
    recommendations = _common_recos(band) + _condition_specific(condition, band)
    return {
        "condition": condition,
        "risk_score": float(risk_score_0_100),
        "risk_band": band,
        "recommendations": recommendations,
    }


