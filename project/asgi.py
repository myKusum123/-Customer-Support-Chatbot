import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chatbot.routing  # Import your app's routing module

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')  # Ensure this points to your settings module

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Handle HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Chatbot_app.routing.websocket_urlpatterns  # Handle WebSocket connections
        )
    ),
})
