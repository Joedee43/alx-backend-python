#!/usr/bin/env python3
"""Unit tests for the client module, testing GithubOrgClient functionality."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from client import GithubOrgClient
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient class."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name: str, mock_get_json) -> None:
        """Test that GithubOrgClient.org returns the expected value and calls get_json once."""
        test_payload = {"payload": True}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self) -> None:
        """Test that GithubOrgClient._public_repos_url returns the expected repos_url from org."""
        test_payload = {"repos_url": "https://api.github.com/orgs/test_org/repos"}
        with patch('client.GithubOrgClient.org', new_callable=Mock) as mock_org:
            mock_org.return_value = test_payload
            client = GithubOrgClient("test_org")
            result = client._public_repos_url
            self.assertEqual(result, test_payload["repos_url"])


if __name__ == "__main__":
    unittest.main()