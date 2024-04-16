import requests
from users.models import User
from urllib.parse import urlparse
import os
from telegram import Bot, ReplyKeyboardMarkup

def extract_domain(url):
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc
    domain = f"{scheme}://{netloc}/"
    return domain

def domain_validate_and_normalize(old_domain:str) -> tuple[bool,str]:
    if old_domain.find("http://") == -1 and old_domain.find("https://") == -1:
        return False, "Домен должен включать http:// или https:// и иметь вид https://api.taiga.io/"
    if old_domain[-1] != '/':
        old_domain+='/'
    old_domain = extract_domain(url=old_domain)
    try:
        data = {
            "password": "abracadanra",
            "type": "normal",
            "username": "abracadanra"
        }
        response = requests.post(old_domain+"api/v1/auth", data=data)
        print(old_domain+"api/v1/auth")
        print(response.status_code)
        print(response.content)
        no_taiga_msg = "Это домен не тайги. Если вы уверены, что на этом сервере тайга - обратитесь к администратору бота"
        if response.status_code not in (401, 429):
            
            return False, no_taiga_msg
    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.ConnectionError):
            
            return False, "Не можем связаться с вашим сервером. Введите правильный домен или разбудите сервер"

    return True, old_domain
def get_auth_refresh_id_via_username(domain: str, username: str, password: str) -> tuple[int, str]:
    print(domain)
    endpoint = "api/v1/auth"
    data = {
        "type": "normal",
        "username": username,
        "password": password
    }
    response = requests.post(url=domain+endpoint, data=data)
    status_code = response.status_code
    print(status_code)
    if status_code == 200:
        response_data = response.json()
        print("RESPONSE_DATA", response_data)
        auth_token = response_data.get("auth_token")
        refresh = response_data.get("refresh")
        return status_code, auth_token, refresh, str(response_data.get("id"))
    return status_code, "", "", ""

def set_taiga_user_data(tg_id, domain,auth_type, refresh=None, application_token=None, auth_token=None, taiga_id=None):
    user = User.objects.get(user_id=tg_id)
    user.domain = domain
    user.taiga_id = taiga_id
    user.is_taiga_auth = True
    if auth_type == "Bearer":
        user.auth_type = "Bearer"
        user.refresh_token = refresh
        user.auth_token = auth_token
    else:
        user.auth_type = "Application"
        user.application_token = application_token
    user.save()
    send_success_auth_msg(user.user_id)
    

def make_start_keyboard() -> ReplyKeyboardMarkup:
    markup = ReplyKeyboardMarkup([
        [
            "/start"
        ]
    ], resize_keyboard=True)
    return markup


def send_success_auth_msg(chat_id):
    """_summary_
    Отправляет пользователю сообщение об успешной авторизации в тайге
    """
    bot_token = os.getenv("TELEGRAM_TOKEN")
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text="Поздравляем, авторизация завершена", reply_markup=make_start_keyboard())
