import requests
import os
import base64

BASE_URL = "http://localhost:8000"
API_KEY = "GUVI-AI-2026"

def test_health():
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Health test failed: {e}")

def test_analyze():
    print("\nTesting document-analyze endpoint...")
    
    # Simple test data
    test_content = "This is a test invoice from ABC Corp to John Doe for $100 on 2026-05-10."
    base64_content = base64.b64encode(test_content.encode()).decode()
    
    payload = {
        "fileName": "test.txt",
        "fileType": "txt",
        "fileBase64": base64_content
    }
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/document-analyze", 
            json=payload,
            headers=headers
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response Structure: {list(response.json().keys())}")
        print(f"Entities Found: {response.json().get('entities')}")
    except Exception as e:
        print(f"Analyze test failed: {e}")

if __name__ == "__main__":
    test_health()
    test_analyze()
