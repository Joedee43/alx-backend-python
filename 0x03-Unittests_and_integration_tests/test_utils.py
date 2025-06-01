#!/usr/bin/env python3
"""Unit tests for the utils module, covering access_nested_map, get_json, and memoize."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
from typing import Mapping, Sequence, Any, Dict


class TestAccessNestedMap(unittest.TestCase):
    """Test case for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """Test that access_nested_map returns the expected value for a given nested map and path."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), "'a'"),
        ({"a": 1}, ("a", "b"), "'b'"),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence,
                                        expected_key: str) -> None:
        """Test that access_nested_map raises KeyError with the correct key for invalid paths."""
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(str(context.exception), expected_key)


class TestGetJson(unittest.TestCase):
    """Test case for the get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict[str, bool]) -> None:
        """Test that get_json returns the expected JSON payload and calls requests.get once."""
        mock = Mock()
        mock.json.return_value = test_payload
        with patch('requests.get', return_value=mock) as mock_get:
            result = get_json(test_url)
            mock_get.assert_called_once_with(test_url)
            self.assertEqual(result, test_payload)


class TestClass:
    """Helper class for testing the memoize decorator."""

    def a_method(self) -> int:
        """Return a constant integer value for testing memoization."""
        return 40

    @memoize
    def a_property(self) -> int:
        """Memoized property that calls a_method."""
        return self.a_method()


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator."""

    def test_memoize(self) -> None:
        """Test that memoize caches the result of a method and calls it only once."""
        obj = TestClass()
        with patch.object(obj, 'a_method', return_value=43) as mocked_method:
            result1 = obj.a_property
            result2 = obj.a_property
            self.assertEqual(result1, 43)
            self.assertEqual(result2, 43)
            mocked_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()