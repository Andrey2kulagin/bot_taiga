


### Как поднять


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
