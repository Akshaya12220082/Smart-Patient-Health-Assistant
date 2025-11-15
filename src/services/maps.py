from __future__ import annotations

from typing import Any, Dict, List

import googlemaps

from src.utils import load_config


CONDITION_TO_KEYWORDS = {
    "diabetes": ["hospital", "endocrinology", "diabetes clinic"],
    "heart": ["hospital", "cardiology", "heart clinic"],
    "kidney": ["hospital", "nephrology", "kidney clinic"],
}


def find_hospitals_nearby(lat: float, lng: float, condition: str, radius_m: int = 5000, config_path: str | None = None) -> List[Dict[str, Any]]:
    cfg = load_config() if config_path is None else load_config(config_path)
    api_key = cfg["api"]["google_maps_api_key"]
    
    # Check if API key is actually set
    if not api_key or api_key.startswith("${"):
        raise ValueError("Google Maps API key not configured. Please set GOOGLE_MAPS_API_KEY environment variable.")
    
    gmaps = googlemaps.Client(key=api_key)

    keywords = CONDITION_TO_KEYWORDS.get(condition.lower(), ["hospital"])
    results: List[Dict[str, Any]] = []
    for keyword in keywords:
        places = gmaps.places_nearby(location=(lat, lng), radius=radius_m, keyword=keyword, type="hospital")
        for p in places.get("results", []):
            results.append({
                "name": p.get("name"),
                "rating": p.get("rating"),
                "user_ratings_total": p.get("user_ratings_total"),
                "address": p.get("vicinity"),
                "place_id": p.get("place_id"),
                "location": p.get("geometry", {}).get("location", {}),
            })

    # Deduplicate by place_id and sort by rating desc then ratings count
    unique = {}
    for r in results:
        unique[r["place_id"]] = r
    deduped = list(unique.values())
    deduped.sort(key=lambda x: (x.get("rating", 0) or 0, x.get("user_ratings_total", 0) or 0), reverse=True)
    return deduped


