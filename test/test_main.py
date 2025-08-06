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

    def test_format_json_valid(self):
        """Test formatting a valid JSON string."""
        json_string = '{"name":"John","age":30,"city":"New York"}'
        response = self.client.post("/format", json={"json_string": json_string})
        self.assertEqual(response.status_code, 200)
        expected_formatted = (
            '{\n  "name": "John",\n  "age": 30,\n  "city": "New York"\n}'
        )
        self.assertEqual(response.json()["formatted"], expected_formatted)

    def test_format_json_nested(self):
        """Test formatting a nested JSON string."""
        json_string = '{"user":{"name":"Alice","details":{"age":25,"skills":["Python","FastAPI"]}}}'
        response = self.client.post("/format", json={"json_string": json_string})
        self.assertEqual(response.status_code, 200)
        result = response.json()["formatted"]
        # Check that it's properly formatted (contains newlines and proper indentation)
        self.assertIn("\n", result)
        self.assertIn('  "user":', result)
        self.assertIn('    "name": "Alice"', result)

    def test_format_json_array(self):
        """Test formatting a JSON array."""
        json_string = '[{"id":1,"name":"Item1"},{"id":2,"name":"Item2"}]'
        response = self.client.post("/format", json={"json_string": json_string})
        self.assertEqual(response.status_code, 200)
        result = response.json()["formatted"]
        self.assertIn("[\n", result)
        self.assertIn("  {\n", result)

    def test_format_json_invalid(self):
        """Test formatting an invalid JSON string."""
        json_string = '{"name":"John","age":30,}'  # Trailing comma makes it invalid
        response = self.client.post("/format", json={"json_string": json_string})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid JSON string", response.json()["detail"])

    def test_format_json_empty_string(self):
        """Test formatting an empty string."""
        json_string = ""
        response = self.client.post("/format", json={"json_string": json_string})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid JSON string", response.json()["detail"])

    def test_format_json_malformed(self):
        """Test formatting a malformed JSON string."""
        json_string = '{"name": "John", "age": 30'  # Missing closing brace
        response = self.client.post("/format", json={"json_string": json_string})
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid JSON string", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
