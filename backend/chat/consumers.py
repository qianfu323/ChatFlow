import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Room, Message
from django.contrib.auth.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    """
    handle websocket message
    """

    async def connect(self):
        """
        connect handler
        """
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'

        # join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """
        disconnect handler
        """
        # leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        """
        receive handler
        """
        if text_data:
            # {"type":"group","room_id":"1","sender_id":1,"username":"yaphp","message":"213","timestamp":1764250832081}
            print("Received:" + text_data)

            data_json = json.loads(text_data)

            # get data param
            room_id = data_json.get('room_id', '')
            sender_id = data_json.get('sender_id', '')
            content = data_json.get('message', '')

            # save to mysql
            if room_id and content:
                # receiver_id=receiver_id

                await self.save_message(
                    room_id=self.room_id,
                    sender_id=sender_id,
                    content=content
                )

            # send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data_json
                }
            )

    @database_sync_to_async
    def save_message(self, room_id, sender_id, content):
        """
        save message to db
        """
        try:
            room = Room.objects.get(id=room_id)
            sender = User.objects.get(id=sender_id)

            # create message obj
            message = Message.objects.create(
                room=room,
                sender=sender,
                content=content
            )

            # update last message timestamp
            room.last_message_at = timezone.now()
            room.save()

            return message
        except (Room.DoesNotExist, User.DoesNotExist) as e:
            print(f"Error saving message: {e}")
            return None

    async def chat_message(self, event):
        """
        handle message from room group
        """
        # send message to client
        await self.send(text_data=json.dumps(event['message']))