import requests

# Simple health check
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"Health check: {response.status_code}")
    print(response.json())
except Exception as e:
    print(f"Health check failed: {e}")

# Test chat with timeout
try:
    print("\nTesting chat endpoint...")
    response = requests.post(
        "http://localhost:8000/api/chat",
        json={"message": "Hi"},
        timeout=30  # 30 second timeout
    )
    print(f"Chat status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Error response: {response.text}")
except requests.exceptions.Timeout:
    print("Request timed out after 30 seconds")
except Exception as e:
    print(f"Chat test failed: {e}")
