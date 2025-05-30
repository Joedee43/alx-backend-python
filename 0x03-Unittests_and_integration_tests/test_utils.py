import unittest
from parameterized import parameterized
from utils import access_nested_map
from unittest.mock import patch, Mock
from utils import get_json
from utils import memoize

# class TestAccessNestedMap(unittest.TestCase):

#     @parameterized.expand([
#         ({"a": 1}, ("a",), 1),
#         ({"a": {"b": 2}}, ("a",), {"b": 2}),
#         ({"a": {"b": 2}}, ("a", "b"), 2),
#     ])
#     def test_access_nested_map(self, nested_map, path, expected):
#         self.assertEqual(access_nested_map(nested_map, path), expected)


#     @parameterized.expand([
#         ({}, ("a",), "'a'"),
#         ({"a": 1}, ("a", "b"), "'b'"),
#     ])
#     def test_access_nested_map_exception(self, nested_map, path, expected_key):
#         with self.assertRaises(KeyError) as context:
#             access_nested_map(nested_map, path)
#         self.assertEqual(str(context.exception), expected_key)

# class TestGetJson(unittest.TestCase):
#     @parameterized.expand([
#         ("http://example.com", {"payload": True}),
#         ("http://holberton.io", {"payload": False}),
#     ])
#     def test_get_json(self, test_url, test_payload):
#         mock = Mock()
#         mock.json.return_value = test_payload
#         with patch('requests.get', return_value=mock) as mock_get:
#             result = get_json(test_url)
#             mock_get.assert_called_once_with(test_url)
#             self.assertEqual(result, test_payload)


class TestClass:
    def a_method(self):
        return 40

    @memoize
    def a_property(self):
        return self.a_method()


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        obj = TestClass()

        # Patch a_method to monitor how often it's called
        with patch.object(obj, 'a_method', return_value=43) as mocked_method:
            # First call should call a_method
            result1 = obj.a_property
            # Second call should use cached result
            result2 = obj.a_property

            # Both results should be equal to the mocked return
            self.assertEqual(result1, 43)
            self.assertEqual(result2, 43)

            # a_method should be called only once due to memoization
            mocked_method.assert_called_once()
if __name__ == "__main__":
    unittest.main()