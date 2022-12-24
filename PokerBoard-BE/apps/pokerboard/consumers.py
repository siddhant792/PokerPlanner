import json
from datetime import datetime

from django.contrib.auth.models import AnonymousUser
from django.db.models.query_utils import Q

from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework import serializers

from apps.pokerboard import (
    constants as pokerboard_constants,
    models as pokerboard_models,
    serializers as pokerboard_serializers,
    utils as pokerboard_utils,
)
from apps.user import serializers as user_serializers


class SessionConsumer(AsyncWebsocketConsumer):
    """
    Session consumer for handling websocket connections
    """
    async def connect(self):
        """
        Runs on connection initiate
        """
        session_id = self.scope['url_route']['kwargs']['pk']
        self.room_name = str(session_id)
        self.group_name = f"session_{self.room_name}"
        self.session = pokerboard_models.GameSession.objects.filter(id=session_id).first()
        if not self.session:
            self.close()
            return

        if type(self.scope["user"]) == AnonymousUser or self.session.status != pokerboard_models.GameSession.IN_PROGRESS:
            self.close()
            return
  
        pokerboards = pokerboard_models.Pokerboard.objects.filter(
            Q(manager=self.scope["user"]) | Q(invite__invitee=self.scope["user"], invite__is_accepted=True)
        )

        if not pokerboards.filter(id=self.session.ticket.pokerboard.id).exists():
            self.close()
            return
        
        # Join room group
        clients = getattr(self.channel_layer, self.group_name, [])
        clients.append(self.scope["user"])
        setattr(self.channel_layer, self.group_name, clients)
        serializer = user_serializers.UserSerializer(clients, many=True)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        message = {
            'type': 'broadcast',
            'message': {
                'type': 'update',
                'users': serializer.data
            }
        }
        await self.accept()
        await self.channel_layer.group_send(
            self.group_name, message
        )

    def estimate(self, event):
        """
        Finalize estimation of a ticket
        """
        try:
            manager = self.session.ticket.pokerboard.manager
            if self.scope["user"] == manager and self.session.status == pokerboard_models.GameSession.IN_PROGRESS:
                self.session.status = pokerboard_models.GameSession.ESTIMATED
                ticket = self.session.ticket
                ticket.estimate = event["message"]["estimate"]
                url = f"{pokerboard_constants.JIRA_API_URL_V2}issue/{ticket.ticket_id}"
                data = json.dumps({
                    "update": {
                        'customfield_10016': [
                            {
                                "set": ticket.estimate
                            }
                        ]
                    }
                })
                self.session.save()
                ticket.save()
                return {
                    "type": event["type"],
                    "estimate": event["message"]["estimate"]
                }
            else:
                self.send(text_data=json.dumps({
                    "error": "Only manager can finalize estimate"
                }))
        except serializers.ValidationError as e:
            self.send(text_data=json.dumps({
                "error": "Estimation failed"
            }))

    def skip(self, event):
        """
        Skip current voting session
        """
        manager = self.session.ticket.pokerboard.manager
        if self.scope["user"] == manager and self.session.status == pokerboard_models.GameSession.IN_PROGRESS:
            self.session.status = pokerboard_models.GameSession.SKIPPED
            self.session.timer_started_at = None
            self.session.save()
            pokerboard_utils.move_ticket_to_end(self.session.ticket)
            return {
                "type": event["type"],
            }
        else:
            self.send(text_data=json.dumps({
                "error": "Can't skip"
            }))
        
    def initialise_game(self, event):
        """
        Initialise game, fetches connceted users and votes already given
        """
        votes = pokerboard_models.Vote.objects.filter(game_session=self.session)
        vote_serializer = pokerboard_serializers.VoteSerializer(instance=votes, many=True)
        clients = list(set(getattr(self.channel_layer, self.group_name, [])))
        serializer = user_serializers.UserSerializer(instance=clients, many=True)
        return {
            "type": event["type"],
            "votes": vote_serializer.data,
            "users": serializer.data,
            "timer": json.dumps(self.session.timer_started_at, default=self.myconverter)
        }

    def vote(self, event):
        """
        Places/update a vote on a ticket
        """
        try:
            serializer = pokerboard_serializers.VoteSerializer(data=event["message"])
            serializer.is_valid(raise_exception=True)
            pokerboard_utils.validate_vote(
                self.session.ticket.pokerboard.estimation_type, serializer.validated_data["estimate"])
            serializer.save(game_session=self.session, user=self.scope["user"])
            return {
                "type": event["type"],
                "vote": serializer.data
            }
        except serializers.ValidationError as e:
            self.send(text_data=json.dumps({
                "error": "Invalid estimate"
            }))

    def start_timer(self, event):
        """
        Starts timer on current voting session
        """
        manager = self.session.ticket.pokerboard.manager
        if self.scope["user"] == manager and self.session.status == pokerboard_models.GameSession.IN_PROGRESS:
            now = datetime.now()
            self.session.timer_started_at = now
            self.session.save()
            return {
                "type": event["type"],
                "timer_started_at": json.dumps(now, default=self.myconverter),
            }
        else:
            self.send(text_data=json.dumps({
                "error": "Can't start timer"
            }))

    def myconverter(self, obj):
        """
        convert datetime into json
        """
        if isinstance(obj, datetime):
            return obj.__str__()

    async def receive(self, text_data):
        """
        Runs on recieving any message, acts as a gateway of websocket communication
        """
        try:
            text_data_json = json.loads(text_data)
            print(text_data_json)
            serializer = pokerboard_serializers.MessageSerializer(data=text_data_json)
            serializer.is_valid(raise_exception=True)
            message = text_data_json['message']
            message_type = text_data_json['message_type']
            method_to_call = getattr(self, message_type)
            res = method_to_call({
                'type': message_type,
                'message': message,
                'user': self.scope["user"].id
            })
            # Send message to room group
            if res:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'broadcast',
                        'message': res
                    }
                )
        except serializers.ValidationError:
            await self.send(text_data=json.dumps({
                "error": "Something went wrong"
            }))

    async def broadcast(self, event):
        """
        Broadcast a message to connected channels in current group
        """
        await self.send(text_data=json.dumps(event["message"]))

    async def disconnect(self, code):
        """
        Runs when a user disconnects
        """
        clients = getattr(self.channel_layer, self.group_name, [])
        clients.remove(self.scope["user"])
        setattr(self.channel_layer, self.group_name, clients)
        serializer = user_serializers.UserSerializer(list(set(clients)), many=True)
        message = {
            'type': 'broadcast',
            'message': {
                'type': 'update',
                'users': serializer.data
            }
        }
        await self.channel_layer.group_send(
            self.group_name, message
        )
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
