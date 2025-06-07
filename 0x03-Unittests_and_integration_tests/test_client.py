#!/usr/bin/env python3
"""Unit and integration tests for the client module, testing GithubOrgClient functionality."""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, Mock
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos
from typing import Dict, List, Mapping


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

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json) -> None:
        """Test that GithubOrgClient.public_repos returns the expected list of repository names."""
        test_repos_url = "http://mocked/repos"
        test_payload = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        mock_get_json.return_value = test_payload
        with patch('client.GithubOrgClient._public_repos_url', return_value=test_repos_url) as mock_repos_url:
            client = GithubOrgClient("test_org")
            result = client.public_repos()
            self.assertEqual(result, ["repo1", "repo2"])
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(test_repos_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: Mapping, license_key: str, expected: bool) -> None:
        """Test that GithubOrgClient.has_license returns whether the repo has the specified license."""
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test case for the GithubOrgClient class, testing public_repos with fixtures."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up class by mocking requests.get to return fixture payloads based on URL."""
        cls.get_patcher = patch('requests.get')
        cls.mock_get = cls.get_patcher.start()

        def get_json_side_effect(url: str) -> Dict:
            """Return appropriate fixture payload based on URL."""
            if url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            elif url == f"https://api.github.com/orgs/test_org":
                return cls.org_payload
            return {}

        cls.mock_get.return_value.json.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class by stopping the requests.get patcher."""
        cls.get_patcher.stop()

    def test_public_repos(self) -> None:
        """Test that public_repos returns the expected list of repository names."""
        client = GithubOrgClient("test_org")
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """Test that public_repos with apache-2.0 license returns the expected repositories."""
        client = GithubOrgClient("test_org")
        result = client.public_repos(license="apache-2.0")
        self.assertEqual(result, self.apache2_repos)


if __name__ == "__main__":
    unittest.main()