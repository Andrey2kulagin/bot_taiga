{'action': 'create', 'type': 'issue', 'by': {'id': 593026, 'permalink': 'https://tree.taiga.io/profile/andrey2kulagin', 'username': 'andrey2kulagin', 'full_name': 'andrey', 'photo': None, 'gravatar_id': '3e937fc01c27b1ba561033d174ada2cd'}, 'date': '2024-04-24T15:06:45.700Z', 'data': {'custom_attributes_values': {}, 'id': 1759994, 'ref': 38, 'created_date': '2024-04-24T15:06:45.591Z', 'modified_date': '2024-04-24T15:06:45.612Z', 'finished_date': None, 'due_date': None, 'due_date_reason': '', 'subject': 'я', 'external_reference': None, 'watchers': [], 'description': 'я', 'tags': [], 'permalink': 'https://tree.taiga.io/project/andrey2kulagin-our-bot/issue/38', 'project': {'id': 1127272, 'permalink': 'https://tree.taiga.io/project/andrey2kulagin-our-bot', 'name': 'our bot', 'logo_big_url': None}, 'milestone': None, 'owner': {'id': 593026, 'permalink': 'https://tree.taiga.io/profile/andrey2kulagin', 'username': 'andrey2kulagin', 'full_name': 'andrey', 'photo': None, 'gravatar_id': '3e937fc01c27b1ba561033d174ada2cd'}, 'assigned_to': {'id': 593026, 'permalink': 'https://tree.taiga.io/profile/andrey2kulagin', 'username': 'andrey2kulagin', 'full_name': 'andrey', 'photo': None, 'gravatar_id': '3e937fc01c27b1ba561033d174ada2cd'}, 'status': {'id': 7894612, 'name': 'New', 'slug': 'new', 'color': '#70728F', 'is_closed': False}, 'type': {'id': 3391300, 'name': 'Bug', 'color': '#E44057'}, 'priority': {'id': 3384696, 'name': 'Normal', 'color': '#E4CE40'}, 'severity': {'id': 5633961, 'name': 'Normal', 'color': '#40E47C'}, 'promoted_to': []}}
 {'action': 'create', 'type': 'issue', 'by': {'id': 593026, 'permalink': 'https://tree.taiga.io/profile/andrey2kulagin', 'username': 'andrey2kulagin', 'full_name': 'andrey', 'photo': None, 'gravatar_id': '3e937fc01c27b1ba561033d174ada2cd'}, 'date': '2024-04-24T15:06:45.700Z', 'data': {'custom_attributes_values': {}, 'id': 1759994, 'ref': 38, 'created_date': '2024-04-24T15:06:45.591Z', 'modified_date': '2024-04-24T15:06:45.612Z', 'finished_date': None, 'due_date': None, 'due_date_reason': '', 'subject': 'я', 'external_reference': None, 'watchers': [], 'description': 'я', 'tags': [], 'permalink': 'https://tree.taiga.io/project/andrey2kulagin-our-bot/issue/38', 'project': {'id': 1127272, 'permalink': 'https://tree.taiga.io/project/andrey2kulagin-our-bot', 'name': 'our bot', 'logo_big_url': None}, 'milestone': None, 'owner': {'id': 593026, 'permalink': 'https://tree.taiga.io/profile/andrey2kulagin', 'username': 'andrey2kulagin', 'full_name': 'andrey', 'photo': None, 'gravatar_id': '3e937fc01c27b1ba561033d174ada2cd'}, 'assigned_to': {'id': 593026, 'permalink': 'https://tree.taiga.io/profile/andrey2kulagin', 'username': 'andrey2kulagin', 'full_name': 'andrey', 'photo': None, 'gravatar_id': '3e937fc01c27b1ba561033d174ada2cd'}, 'status': {'id': 7894612, 'name': 'New', 'slug': 'new', 'color': '#70728F', 'is_closed': False}, 'type': {'id': 3391300, 'name': 'Bug', 'color': '#E44057'}, 'priority': {'id': 3384696, 'name': 'Normal', 'color': '#E4CE40'}, 'severity': {'id': 5633961, 'name': 'Normal', 'color': '#40E47C'}, 'promoted_to': []}}

# Особенности, преимущества и просто заметки
## Что это за папки?
login, users - это папки django-приложений. dtb - основная django-папка, где настройки проекта
tgbot - здесь весь бот
ustils - сюда вынесены вся(или почти вся) бизнес-логика(Функции, которые выполняют основные задачи пользователей)
## Основное
У нас несколько моделей, есть встроенные, есть добавленные автором шаблона
Нам надо обратить внимание на users.models.User
Это пользователь бота, поля можно посмотреть в модели
Объект этой модели автоматически создается, когда юзер что-то пишет боту и этот объект потом обновляется во время авторизации в тайгу.
Авторизация происходит по адресу 127.0.0.1:8000/taiga_login/standard или 127.0.0.1:8000/taiga_login/application в зависимости от типа авторизации. При авторизации надо указать query-параметры domain=https://api.taiga.io/&tg_id=6043590166

Админка назодится по адресу 127.0.0.1:8000/
# Как поднять


Самый простой способ - поднять виртуалку с ubuntu(18-22) и на ней установить docker и docker-compose
Дальше надо скопировать .env_example и назвать его .env
``` bash
cp .env_example .env
```
Вставить в него надо примерно следующее:
```
DJANGO_DEBUG=True
DATABASE_URL=postgres://postgres:postgres@db:5432/postgres
TELEGRAM_TOKEN=1725447442:AATuNIAicSPdePxxTHdbO1X_4hfAnONOyiA
```
TELEGRAM_TOKEN должен быть свой, получить его можно в tg @BotFather
Чтобы поднять нужно просто ввести команду
``` bash
docker-compose up -d --build
```
Чтобы создать админа надо посмотреть всё, что запущено
``` bash
docker ps -a
```
Примерно вот так будет выглядеть:
<p align="left">
    <img src="https://github.com/ohld/django-telegram-bot/raw/main/.github/imgs/containers_status.png">
</p>

Там надо найти что-то, где есть слово web и скопировать id контейнера(вместо 44a0791a59fc) в команду:

``` bash
docker exec -it 44a0791a59fc bash
```

Это открылся стандартный django-терминал, далее просто создаем все как обычно

``` bash
python manage.py createsuperuser
```
И вот так делаются миграции

``` bash
python manage.py makemigrations
python manage.py migrate
```
