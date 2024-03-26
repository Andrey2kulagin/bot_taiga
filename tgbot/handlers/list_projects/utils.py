from utils.taiga_back.lists_project import list_project
from users.models import User


def get_projects(tg_id):
    '''
    call some db function and give it tg user id, get the taiga user id
    get the token
    скорее всего работа с бд где-то тут users.models.User.get_user_and_created
    этот метод дергает какой-то коллбек

    посмотреть штуку которая пишет в бд при авторизации
    это где-то немного вебморда джанги
    '''
    user = User.objects.get(user_id=tg_id)
    if user.auth_type == "Bearer":
        projects = list_project(user.auth_token, user.taiga_id)
    else:
        projects = list_project(user.application_token, user.taiga_id)
    return projects

def format_projects(projects):
    '''
    Форматирует список проектов в красивый текстовый формат.
    :param projects: список проектов в формате [{"id": int, "name": str}]
    :return: строка, содержащая информацию о проектах
    TODO: заменить текст захардкоженный текст на динамический
    '''
    if not projects:
        return "У вас нет проектов."

    if "Ошибка: 401" in projects:
        return "Ваш токен истек."
    
    projects_str = "Ваши проекты:\n\n"
    count = 1
    for project in projects:
        projects_str += f"{count}. ID: {project['id']} - Название: {project['name']}\n"
        count += 1
    projects_str += "\nВыберете проект для продолжения работы."

    return projects_str

def get_taiga_token_by_tg_id(tg_id):
    user = User.objects.get(user_id=tg_id)
    if user.auth_type == "Bearer":
        return user.auth_token
    else:
        return user.application_token
