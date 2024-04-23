from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from webhook.utils import parse_taiga_webhook
from django.views.decorators.csrf import csrf_exempt


class WebhookReceiver(APIView):
    # https://stackoverflow.com/questions/17716624/django-csrf-cookie-not-set
    # @csrf_exempt
    def post(self, request, format=None):
        data = request.data  # Получаем данные из POST-запроса
        print(data)
        print(parse_taiga_webhook(data))
        return Response(status=status.HTTP_200_OK)              