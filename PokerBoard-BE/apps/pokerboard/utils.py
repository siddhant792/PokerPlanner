import json
import requests
from typing import Any

from rest_framework.serializers import ValidationError

from apps.pokerboard import (
    constants as pokerboard_constants,
    models as pokerboard_models
)


class JiraApi:
    """
    Jira API Utilities
    """

    @staticmethod
    def query_jira(method: str, url: str, payload: Any=None, status_code: int=200):
        """
        Perform a request and returns response
        """
        if not payload:
            payload = {}
        response = requests.request(method, url, auth=pokerboard_constants.JIRA_AUTH, headers=pokerboard_constants.JIRA_HEADERS, data=payload)
        if response.status_code != status_code:
            error_msgs = ["Something went wrong"]
            res = json.loads(response.text)
            error_msgs = res.get("errorMessages", error_msgs)
            raise ValidationError(error_msgs)
        if not response.text:
            return {}
        return json.loads(response.text)

    @staticmethod
    def get_sprints(boardId: int) -> list:
        """
        Get sprints for a given board
        """
        sprint_res = JiraApi.query_jira("GET", f"{pokerboard_constants.JIRA_API_URL_V1}board/{boardId}/sprint")
        return sprint_res["values"]

    @staticmethod
    def get_boards() -> list:
        """
        Get all available boards
        """
        boards_url = f"{pokerboard_constants.JIRA_API_URL_V1}board"
        boards_res = JiraApi.query_jira("GET", boards_url)
        return boards_res["values"]

    @staticmethod
    def get_all_sprints() -> list:
        """
        Fetches all sprints from all available boards
        """
        boards = JiraApi.get_boards()
        sprints = []
        for board in boards:
            sprints = sprints + JiraApi.get_sprints(board["id"])
        return sprints


def validate_vote(deck_type: int, estimate: int) -> None:
    """
    Validates a vote based on deck type
    """
    if deck_type == pokerboard_models.Pokerboard.EVEN:
        if estimate % 2 == 1:
            raise ValidationError("Invalid estimate")
    elif deck_type == pokerboard_models.Pokerboard.ODD:
        if estimate % 2 == 0:
            raise ValidationError("Invalid estimate")
    elif deck_type == pokerboard_models.Pokerboard.FIBONACCI:
        if estimate not in pokerboard_constants.FIBONACCI_OPTIONS:
            raise ValidationError("Invalid estimate")


def move_ticket_to_end(ticket: pokerboard_models.Ticket) -> None:
    """
    move a ticket to the end of the list
    """
    # costs 2 db hits
    all_tickets = ticket.pokerboard.tickets.filter(rank__gte=ticket.rank, estimate=None).order_by('rank')
    prev_rank = ticket.rank
    for _ticket in all_tickets:
        if _ticket.rank == prev_rank:
            continue
        _ticket.rank, prev_rank = prev_rank, _ticket.rank
    
    all_tickets.first().rank = prev_rank
    pokerboard_models.Ticket.objects.bulk_update(all_tickets, ['rank'])
