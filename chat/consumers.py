import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)

        # Typing indicator handling
        if 'typing' in data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_typing',
                    'typing': data['typing'],
                    'user': data.get('user', 'Anonymous'),
                    'role': data.get('role', '')
                }
            )
            return

        # Regular chat message
        message = data.get('message', '')
        user = data.get('user', 'Anonymous')
        role = data.get('role', '')
        system = data.get('system', False)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user,
                'role': role,
                'system': system
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
            'role': event.get('role', ''),
            'system': event.get('system', False)
        }))

    async def chat_typing(self, event):
        await self.send(text_data=json.dumps({
            'typing': event['typing'],
            'user': event['user'],
            'role': event['role']
        }))
 