"""
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()


# Start the local IRC server in the background
import threading
import asyncio
import sys
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from home.routing import websocket_urlpatterns

def start_local_irc_server():
    from local_irc_server import irc_server_instance
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(irc_server_instance.start())
    except Exception as e:
        print(f"[IRC Server] Error: {e}", file=sys.stderr)

# Only start the IRC server once (avoid multiple threads in reload)
if not hasattr(sys, '_irc_server_started'):
    sys._irc_server_started = True
    threading.Thread(target=start_local_irc_server, daemon=True).start()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
