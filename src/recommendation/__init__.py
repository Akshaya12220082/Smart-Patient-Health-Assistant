"""
Recommendation engine for personalized guidance and risk stratification.
"""

from .engine import generate_recommendations, risk_band

__all__ = [
    "generate_recommendations",
    "risk_band",
]

