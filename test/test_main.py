import unittest
from fastapi.testclient import TestClient
from app.main import app


class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello, FastAPI!"})

    def test_divide_valid(self):
        response = self.client.get("/divide?a=10&b=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": 5.0})

    def test_divide_negative(self):
        response = self.client.get("/divide?a=-10&b=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": -5.0})

    def test_divide_float(self):
        response = self.client.get("/divide?a=7.5&b=2.5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": 3.0})


if __name__ == "__main__":
    unittest.main()
