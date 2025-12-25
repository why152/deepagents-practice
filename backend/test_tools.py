import sys
import os

# Ensure we can import from the current directory
sys.path.append(os.getcwd())

from my_agent.tools import analyze_data, fetch_weather, validate_user

def test_analyze_data():
    print("Testing analyze_data...")
    data = [
        {"id": 1, "category": "A", "value": 10},
        {"id": 2, "category": "B", "value": 20},
        {"id": 3, "category": "A", "value": 30},
        {"id": 4, "category": "A", "value": 40},
    ]
    criteria = {"category": "A"}
    result = analyze_data.invoke({"data": data, "criteria": criteria})
    print(f"Result: {result}")
    assert result["count"] == 3
    assert result["averages"]["value"] == 26.666666666666668
    print("analyze_data PASSED\n")

def test_fetch_weather():
    print("Testing fetch_weather...")
    city = "Tokyo"
    result = fetch_weather.invoke({"city": city, "include_forecast": True})
    print(f"Result: {result}")
    assert result["city"] == "Tokyo"
    assert "forecast" in result
    print("fetch_weather PASSED\n")

def test_validate_user():
    print("Testing validate_user...")
    valid_user = {"age": 25, "email": "test@example.com", "username": "user123"}
    result_valid = validate_user.invoke({"user_profile": valid_user})
    print(f"Valid User Result: {result_valid}")
    assert result_valid["is_valid"] is True

    invalid_user = {"age": -5, "email": "bad-email", "username": "yo"}
    result_invalid = validate_user.invoke({"user_profile": invalid_user})
    print(f"Invalid User Result: {result_invalid}")
    assert result_invalid["is_valid"] is False
    assert len(result_invalid["errors"]) == 3
    print("validate_user PASSED\n")

if __name__ == "__main__":
    try:
        test_analyze_data()
        test_fetch_weather()
        test_validate_user()
        print("ALL TESTS PASSED!")
    except Exception as e:
        print(f"TEST FAILED: {e}")
        sys.exit(1)
