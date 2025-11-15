"""
OpenStreetMap (OSM) integration for finding nearby hospitals and medical facilities.
Uses Overpass API - completely free, no API key required.
"""

from typing import Any, Dict, List
import requests
import time


CONDITION_TO_OSM_TAGS = {
    "diabetes": ["hospital", "clinic", "doctors"],
    "heart": ["hospital", "clinic", "doctors"],
    "kidney": ["hospital", "clinic", "doctors"],
}

CONDITION_TO_SPECIALTIES = {
    "diabetes": ["endocrinology", "diabetes", "internal medicine"],
    "heart": ["cardiology", "cardiac", "heart"],
    "kidney": ["nephrology", "kidney", "dialysis"],
}


def find_hospitals_nearby_osm(
    lat: float, lng: float, condition: str, radius_m: int = 5000
) -> List[Dict[str, Any]]:
    """
    Find nearby hospitals using OpenStreetMap Overpass API.
    Completely free, no API key required.
    
    Args:
        lat: Latitude
        lng: Longitude
        condition: Disease type (diabetes, heart, kidney)
        radius_m: Search radius in meters (default 5000)
    
    Returns:
        List of hospitals with name, location, and other details
    """
    
    # Overpass API endpoint
    overpass_url = "https://overpass-api.de/api/interpreter"
    
    # Get specialty keywords for filtering
    specialties = CONDITION_TO_SPECIALTIES.get(condition.lower(), [])
    
    # Build Overpass QL query for medical facilities
    # Search for hospitals, clinics, and doctors within radius
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="hospital"](around:{radius_m},{lat},{lng});
      node["amenity"="clinic"](around:{radius_m},{lat},{lng});
      node["amenity"="doctors"](around:{radius_m},{lat},{lng});
      way["amenity"="hospital"](around:{radius_m},{lat},{lng});
      way["amenity"="clinic"](around:{radius_m},{lat},{lng});
      way["amenity"="doctors"](around:{radius_m},{lat},{lng});
    );
    out center tags;
    """
    
    try:
        response = requests.post(
            overpass_url,
            data={"data": overpass_query},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        
        results = []
        seen_names = set()  # Deduplicate by name
        
        for element in data.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name", "Unnamed Medical Facility")
            
            # Skip if we've already seen this name (duplicate)
            if name in seen_names:
                continue
            
            # Get coordinates (handle both node and way types)
            if element["type"] == "node":
                elem_lat = element.get("lat")
                elem_lng = element.get("lon")
            elif element["type"] == "way" and "center" in element:
                elem_lat = element["center"].get("lat")
                elem_lng = element["center"].get("lon")
            else:
                continue
            
            if not elem_lat or not elem_lng:
                continue
            
            # Build address from OSM tags
            address_parts = []
            if "addr:housenumber" in tags:
                address_parts.append(tags["addr:housenumber"])
            if "addr:street" in tags:
                address_parts.append(tags["addr:street"])
            if "addr:city" in tags:
                address_parts.append(tags["addr:city"])
            
            address = ", ".join(address_parts) if address_parts else "Address not available"
            
            # Get facility type
            amenity = tags.get("amenity", "medical")
            healthcare = tags.get("healthcare", "")
            specialty = tags.get("healthcare:speciality", "")
            
            # Filter by specialty if specified
            if specialties:
                name_lower = name.lower()
                specialty_lower = specialty.lower() if specialty else ""
                healthcare_lower = healthcare.lower() if healthcare else ""
                
                # Check if facility matches the specialty
                is_match = any(
                    spec.lower() in name_lower or 
                    spec.lower() in specialty_lower or 
                    spec.lower() in healthcare_lower
                    for spec in specialties
                )
                
                # Always include general hospitals
                if not is_match and amenity != "hospital":
                    continue
            
            # Calculate distance (approximate)
            distance = calculate_distance(lat, lng, elem_lat, elem_lng)
            
            results.append({
                "name": name,
                "lat": elem_lat,
                "lng": elem_lng,
                "vicinity": address,
                "place_id": f"osm_{element['type']}_{element['id']}",
                "rating": None,  # OSM doesn't have ratings
                "user_ratings_total": 0,
                "amenity": amenity,
                "healthcare": healthcare,
                "specialty": specialty,
                "distance_meters": distance,
                "phone": tags.get("phone", ""),
                "website": tags.get("website", ""),
                "opening_hours": tags.get("opening_hours", ""),
            })
            
            seen_names.add(name)
        
        # Sort by distance
        results.sort(key=lambda x: x["distance_meters"])
        
        return results
    
    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to query OpenStreetMap: {str(e)}")
    except Exception as e:
        raise Exception(f"Error processing OSM data: {str(e)}")


def calculate_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate approximate distance between two points in meters.
    Uses simple Euclidean distance (good enough for small distances).
    """
    from math import sqrt
    
    # Rough conversion: 1 degree ≈ 111,000 meters at equator
    lat_diff = (lat2 - lat1) * 111000
    lng_diff = (lng2 - lng1) * 111000 * 0.9  # Adjust for longitude
    
    return sqrt(lat_diff**2 + lng_diff**2)


def format_osm_results_for_api(results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Format OSM results to match Google Maps API structure for compatibility.
    """
    formatted = []
    for r in results:
        formatted.append({
            "name": r["name"],
            "rating": r.get("rating"),
            "user_ratings_total": r.get("user_ratings_total", 0),
            "vicinity": r["vicinity"],
            "place_id": r["place_id"],
            "lat": r["lat"],
            "lng": r["lng"],
            "distance_km": round(r["distance_meters"] / 1000, 2),
            "phone": r.get("phone", ""),
            "website": r.get("website", ""),
            "opening_hours": r.get("opening_hours", ""),
        })
    return formatted
