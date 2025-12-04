import unittest
import requests

class TestAPI(unittest.TestCase):
    @unittest.skip("Skipping API integration test in CI environment")
    def test_chat_endpoint(self):
        url = "http://localhost:8000/api/chat"
        data = {"message": "Hi, I need car insurance"}
        try:
            response = requests.post(url, json=data)
            self.assertEqual(response.status_code, 200)
        except Exception:
            self.fail("API endpoint not reachable")

if __name__ == "__main__":
    unittest.main()
