# chatbot/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatSession, ChatMessage
from .utils import extract_entities, generate_response_based_on_entities, analyze_sentiment

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.session = await ChatSession.objects.get(session_id=self.session_id)
        self.room_group_name = f'chat_{self.session_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_input = text_data_json['message']
        
        # Process user message
        entities = extract_entities(user_input)
        response = generate_response_based_on_entities(entities)
        sentiment = analyze_sentiment(user_input)
        
        # Save user's message and bot's response
        await self.save_chat_message(self.session, 'User', user_input)
        await self.save_chat_message(self.session, 'Bot', response)
        
        # Send message to WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': response
            }
        )

    async def chat_message(self, event):
        message = event['message']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def save_chat_message(self, session, sender, message_text):
        ChatMessage.objects.create(
            session=session,
            sender=sender,
            message_type='text',
            message=message_text,
            is_read=False
        )
