import json
from channels.generic.websocket import AsyncWebsocketConsumer


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
            print("Received:" + text_data)

            data_json = json.loads(text_data)

            # send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data_json
                }
            )

    async def chat_message(self, event):
        """
        handle message from room group
        """
        # send message to client
        await self.send(text_data=json.dumps(event['message']))
