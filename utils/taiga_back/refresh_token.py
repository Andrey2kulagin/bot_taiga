import requests
from users.models import User
import _json


def refresh_access_token(tg_id: str) -> tuple[int, dict]:
    user = User.objects.get(user_id=tg_id)

    # URL и заголовки для запроса
    url = "https://api.taiga.io/api/v1/auth/refresh"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "refresh": user.refresh_token
    }

    # Отправляем POST-запрос
    response = requests.post(url, headers=headers, json=data)
    print(response)
    return response.status_code, response.json()
