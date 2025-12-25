from __future__ import annotations

from typing import Any, List, Dict

from datetime import datetime, timezone, timedelta
from langchain_core.tools import tool


JST = timezone(timedelta(hours=9))


@tool
def now_jst() -> str:
    """Return current time in JST (ISO8601)."""
    return datetime.now(JST).isoformat()


@tool
def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b


@tool
def analyze_data(data: List[Dict[str, Any]], criteria: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze a list of dictionaries based on criteria.
    Returns count of matches and averages of numeric fields in matches.
    """
    matches = []
    for item in data:
        match = True
        for key, value in criteria.items():
            if item.get(key) != value:
                match = False
                break
        if match:
            matches.append(item)

    result = {"count": len(matches), "averages": {}}
    
    if not matches:
        return result

    # Calculate averages for numeric fields
    keys = matches[0].keys()
    for key in keys:
        if isinstance(matches[0][key], (int, float)):
            total = sum(d[key] for d in matches if isinstance(d.get(key), (int, float)))
            result["averages"][key] = total / len(matches)
            
    return result


@tool
def fetch_weather(city: str, include_forecast: bool = False) -> Dict[str, Any]:
    """
    Fetch (mocked) weather data for a given city.
    """
    # Mock data generation based on city name hash to be deterministic but varied
    base_temp = sum(ord(c) for c in city) % 30
    
    weather_data = {
        "city": city,
        "temperature": base_temp,
        "humidity": (base_temp * 2) % 100,
        "condition": "Sunny" if base_temp > 20 else "Cloudy"
    }
    
    if include_forecast:
        weather_data["forecast"] = [
            {"day": f"Day {i}", "temp": base_temp + i} for i in range(1, 4)
        ]
        
    return weather_data



@tool
def validate_user(user_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate a user profile dictionary.
    Checks: age > 0, email contains '@', username length >= 3.
    """
    errors = []
    
    if "age" in user_profile:
        if not isinstance(user_profile["age"], int) or user_profile["age"] <= 0:
            errors.append("Age must be a positive integer")
    else:
        errors.append("Missing 'age' field")
        
    if "email" in user_profile:
        if "@" not in str(user_profile["email"]):
            errors.append("Invalid email format")
    else:
        errors.append("Missing 'email' field")
        
    if "username" in user_profile:
        if len(str(user_profile["username"])) < 3:
            errors.append("Username must be at least 3 characters")
    else:
        errors.append("Missing 'username' field")
        
    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


@tool
def fetch_external_data(resource: str, id: int = None) -> Dict[str, Any] | List[Dict[str, Any]] | str:
    """
    Fetch data from the JSONPlaceholder API (mock data).
    
    Args:
        resource: The resource to fetch. Supported: 'posts', 'users', 'todos'.
        id: Optional ID of the specific item to fetch.
    """
    base_url = "https://jsonplaceholder.typicode.com"
    valid_resources = ["posts", "users", "todos"]
    
    if resource not in valid_resources:
        return f"Error: Invalid resource '{resource}'. Supported: {', '.join(valid_resources)}"
    
    url = f"{base_url}/{resource}"
    if id is not None:
        url = f"{url}/{id}"
        
    try:
        import requests
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Error fetching data: {str(e)}"


ALL_TOOLS = [now_jst, add, analyze_data, fetch_weather, validate_user, fetch_external_data]
