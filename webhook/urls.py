from django.urls import path
from webhook.views import WebhookReceiver

urlpatterns = [
    path('webhook/', WebhookReceiver.as_view(), name='webhook'),
]