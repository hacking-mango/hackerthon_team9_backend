import os
from django.core.asgi import get_asgi_application # noqa

http_asgi = get_asgi_application() # noqa
from channels.auth import AuthMiddlewareStack # noqa
from channels.routing import ProtocolTypeRouter, URLRouter # noqa

import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings.dev")

application = ProtocolTypeRouter(
    {
        "http": http_asgi,
        "websocket": AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns)),
    }
)

# application = get_asgi_application()
