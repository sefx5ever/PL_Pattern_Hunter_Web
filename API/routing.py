from django.urls import path
from API.consumers import WSDataShare

ws_urlpatterns = [
    path('ws/symbol_channel/', WSDataShare.as_asgi())
]
