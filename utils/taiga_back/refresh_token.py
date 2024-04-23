from typing import Any

import requests
from users.models import User


def refresh_access_token(tg_id: str) -> str | Any:
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

    # десериализуем новые токены
    # TODO: проверить пришел ли ответ с токенами или говно какое-то
    if response.status_code == 200:
        data = response.json()
        new_auth_token = data["auth_token"]
        new_refresh_token = data["refresh"]

        # пишем новые токены в бд
        user.auth_token = new_auth_token
        user.refresh_token = new_refresh_token
        user.save()
        return "Success"
    else:
        return response.status_code
