from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from webhook.utils import parse_taiga_webhook, send_notifications
from django.views.decorators.csrf import csrf_exempt

class WebhookReceiver(APIView):
    # https://stackoverflow.com/questions/17716624/django-csrf-cookie-not-set
    # @csrf_exempt
    def post(self, request, format=None):
        data = request.data  # Получаем данные из POST-запроса
        parsed_data = parse_taiga_webhook(data)

        print(data)
        print(parsed_data)

        send_notifications(data)
        return Response(status=status.HTTP_200_OK)
