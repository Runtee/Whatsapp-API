"""
ASGI config for whatsapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
from channels.routing import ProtocolTypeRouter, URLRouter
import os
import chat.routing


from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'whatsapp.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter(
        chat.routing.websocket_urlpatterns
    ),
})
