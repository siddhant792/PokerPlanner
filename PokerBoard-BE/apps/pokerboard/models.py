from django.contrib.auth import get_user_model
from django.db import models

from apps.user import models as user_models
from apps.group import models as group_models


class Pokerboard(user_models.CustomBase):
    """
    Pokerboard settings class
    """
    SERIES = 1
    EVEN = 2
    ODD = 3
    FIBONACCI = 4
    ESTIMATION_CHOICES = (
        (SERIES, "Series"),
        (EVEN, "Even"),
        (ODD, "Odd"),
        (FIBONACCI, "Fibonacci"),
    )

    CREATED = 1
    STARTED = 2
    ENDED = 3
    STATUS_CHOICES = (
        (CREATED, "Created"),
        (STARTED, "Started"),
        (ENDED, "Ended")
    )
    manager = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, help_text='Owner of Pokerboard')
    title = models.CharField(unique=True, max_length=20, help_text='Name of Pokerboard')
    description = models.CharField(max_length=100, help_text='Description')
    estimation_type = models.IntegerField(choices=ESTIMATION_CHOICES, help_text='Estimation type', default=SERIES)
    duration = models.IntegerField(help_text='Duration for voting (in secs)')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=CREATED)
    
    def __str__(self) -> str:
        return self.title


class Ticket(user_models.CustomBase):
    """
    Ticket details class
    """
    pokerboard = models.ForeignKey(Pokerboard, related_name="tickets", on_delete=models.CASCADE, help_text="Pokerboard to which ticket belongs")
    ticket_id = models.SlugField(help_text="Ticket ID imported from JIRA")
    estimate = models.IntegerField(null=True, help_text="Final estimate of ticket")
    rank = models.PositiveSmallIntegerField(help_text="Rank of ticket")

    def __str__(self) -> str:
        return f'{self.ticket_id} - {self.pokerboard}'


class GameSession(user_models.CustomBase):
    """
    GameSession model for storing each estimation session's details
    """
    IN_PROGRESS = 1
    SKIPPED = 2
    ESTIMATED = 3
    STATUS_CHOICES = (
        (IN_PROGRESS, "In progress"),
        (SKIPPED, "Skipped"),
        (ESTIMATED, "Estimated"),
    )
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="estimations")
    status = models.PositiveIntegerField(default=IN_PROGRESS, choices=STATUS_CHOICES)
    timer_started_at = models.DateTimeField(null=True)

    def __str__(self) -> str:
        return f"{self.ticket.ticket_id} {self.status}"


class Vote(user_models.CustomBase):
    """
    Vote model for storing vote details for each user
    """
    game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="estimations")
    estimate = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'game_session')

    def __str__(self) -> str:
        return f"{self.user} {self.game_session.ticket.ticket_id} {self.estimate}"


class Invite(user_models.CustomBase):
    """
    Invite model => stores invitee details, pokerboard to which invited,
    group_name (if invited through group), role of invitee, whether invitation is accepted
    or not
    """
    EMAIL = 1
    GROUP = 2
    INVITE_TYPE = (
        (EMAIL, "email"),
        (GROUP, "group")
    )
    SPECTATOR = 1
    CONTRIBUTOR = 2
    ROLE = (
        (SPECTATOR, "Spectator"),
        (CONTRIBUTOR, "Contributor"),
    )
    type = models.IntegerField(
        choices=INVITE_TYPE, help_text="Invited through", default=EMAIL
    )
    invitee = models.EmailField(null=True, help_text="Person invited")
    pokerboard = models.ForeignKey(
        Pokerboard, related_name="invite", on_delete=models.CASCADE,
        help_text="Pokerboard"
    )
    group_name = models.CharField(max_length=20, null=True, help_text="Name of group")
    group = models.ForeignKey(
        group_models.Group, on_delete=models.CASCADE, null=True,
        help_text="Name of group through which invited, if invited via group"
    )
    role = models.IntegerField(choices=ROLE, help_text="Role", default=CONTRIBUTOR)
    is_accepted = models.BooleanField(default=False, help_text="Boolean indicates if invitation accepted or not")

    def __str__(self):
        return f'Invitee: {self.invitee} - Pokerboard: {self.pokerboard} - Group: {self.group}'

