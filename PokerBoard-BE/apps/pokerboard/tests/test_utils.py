import json
from unittest.mock import Mock, patch

from rest_framework.test import APITestCase

from apps.pokerboard import (
    utils as pokerboard_utils
)
from apps.pokerboard.tests import mock_data as pokerboard_mock_data


class JiraApiTestCases(APITestCase):
    """
    Test Jira api
    """

    @patch("apps.pokerboard.utils.requests.request")
    def test_get_sprints(self: APITestCase, mock_get: Mock) -> None:
        """
        Test get sprints
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = json.dumps(pokerboard_mock_data.SPRINTS_RESPONSE)
        sprints = pokerboard_utils.JiraApi.get_sprints(1)
        self.assertEqual(sprints, pokerboard_mock_data.SPRINTS_RESPONSE["values"])

    @patch("apps.pokerboard.utils.requests.request")
    def test_get_boards(self: APITestCase, mock_get: Mock) -> None:
        """
        Test get boards
        """
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = json.dumps(pokerboard_mock_data.BOARDS_RESPONSE)
        boards = pokerboard_utils.JiraApi.get_boards()
        self.assertEqual(boards, pokerboard_mock_data.BOARDS_RESPONSE["values"])

    @patch("apps.pokerboard.utils.JiraApi.get_boards")
    @patch("apps.pokerboard.utils.requests.request")
    def test_get_all_sprints(self: APITestCase, mock_get: Mock, boards_mock: Mock) -> None:
        """
        Test get all sprints
        """
        boards_mock.return_value = pokerboard_mock_data.BOARDS_RESPONSE["values"]
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = json.dumps(pokerboard_mock_data.SPRINTS_RESPONSE)
        sprints = pokerboard_utils.JiraApi.get_all_sprints()
        self.assertEqual(sprints, pokerboard_mock_data.SPRINTS_RESPONSE["values"])

