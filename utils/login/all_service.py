import requests
from users.models import User


def domain_validate_and_normalize(old_domain:str) -> tuple[bool,str]:
    if old_domain.find("http://") == -1 and old_domain.find("https://") == -1:
        return False, "Домен должен включать http:// или https:// и иметь вид https://api.taiga.io/"
    if old_domain[-1] != '/':
        old_domain+='/'
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
        if response.status_code != 401 :
            
            return False, no_taiga_msg
        no_taiga_msg = "Это домен не тайги. Если вы уверены, что на этом сервере тайга - обратитесь к администратору бота"
        try:
            data = response.json()
            if data.get("code") != 'invalid_credentials':
                print("Тут")
                return False, no_taiga_msg
        except requests.exceptions.JSONDecodeError as e:
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