# django-telegram-bot

<p align="center">
    <img src="https://user-images.githubusercontent.com/50623190/201977740-68ef4044-9cfa-45da-8897-2a90ecfa33ae.png" align="center" height="350px" weight="350px">
</p>

Sexy Django + python-telegram-bot + Celery + Redis + Postgres + Dokku + GitHub Actions template. Production-ready Telegram bot with database, admin panel and a bunch of useful built-in methods.


⭐ graph: 
[![Sparkline](https://stars.medv.io/ohld/django-telegram-bot.svg)](https://stars.medv.io/ohld/django-telegram-bot)


### Check the example bot that uses the code from Main branch: [t.me/djangotelegrambot](https://t.me/djangotelegrambot)

## Features

* Database: Postgres, Sqlite3, MySQL - you decide!
* Admin panel (thanks to [Django](https://docs.djangoproject.com/en/3.1/intro/tutorial01/))
* Background jobs using [Celery](https://docs.celeryproject.org/en/stable/)
* [Production-ready](https://github.com/ohld/django-telegram-bot/wiki/Production-Deployment-using-Dokku) deployment using [Dokku](https://dokku.com)
* Telegram API usage in polling or [webhook mode](https://core.telegram.org/bots/api#setwebhook)
* Export all users in `.csv`
* Native telegram [commands in menu](https://github.com/ohld/django-telegram-bot/blob/main/.github/imgs/bot_commands_example.jpg)
  * In order to edit or delete these commands you'll need to use `set_my_commands` bot's method just like in [tgbot.dispatcher.setup_my_commands](https://github.com/ohld/django-telegram-bot/blob/main/tgbot/dispatcher.py#L150-L156)

Built-in Telegram bot methods:
* `/broadcast` — send message to all users (admin command)
* `/export_users` — bot sends you info about your users in .csv file (admin command)
* `/stats` — show basic bot stats 
* `/ask_for_location` — log user location when received and reverse geocode it to get country, city, etc.


## Content

* [How to run locally](https://github.com/ohld/django-telegram-bot/#how-to-run)
   * [Quickstart with polling and SQLite](https://github.com/ohld/django-telegram-bot/#quickstart-polling--sqlite)
   * [Using docker-compose](https://github.com/ohld/django-telegram-bot/#run-locally-using-docker-compose)
* [Deploy to production](https://github.com/ohld/django-telegram-bot/#deploy-to-production)
   * [Using dokku](https://github.com/ohld/django-telegram-bot/#deploy-using-dokku-step-by-step)
   * [Telegram webhook](https://github.com/ohld/django-telegram-bot/#https--telegram-bot-webhook)


# How to run

## Quickstart: Polling & SQLite

The fastest way to run the bot is to run it in polling mode using SQLite database without all Celery workers for background jobs. This should be enough for quickstart:

``` bash
git clone https://github.com/ohld/django-telegram-bot
cd django-telegram-bot
```

Create virtual environment (optional)
``` bash
python3 -m venv dtb_venv
source dtb_venv/bin/activate
```

Install all requirements:
```
pip install -r requirements.txt
```

Create `.env` file in root directory and copy-paste this or just run `cp .env_example .env`,
don't forget to change telegram token:
``` bash 
DJANGO_DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
TELEGRAM_TOKEN=<PASTE YOUR TELEGRAM TOKEN HERE>
```

Run migrations to setup SQLite database:
``` bash
python manage.py migrate
```

Create superuser to get access to admin panel:
``` bash
python manage.py createsuperuser
```

Run bot in polling mode:
``` bash
python run_polling.py 
```

If you want to open Django admin panel which will be located on http://localhost:8000/tgadmin/:
``` bash
python manage.py runserver
```

## Run locally using docker-compose
If you want just to run all the things locally, you can use Docker-compose which will start all containers for you.

### Create .env file. 
You can switch to PostgreSQL just by uncommenting it's `DATABASE_URL` and commenting SQLite variable.
```bash
cp .env_example .env
```

### Docker-compose

Как поднять?
Самый простой способ - поднять виртуалку с линуксом и на ней установить docker и docker-compose
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
``` bash
docker-compose up -d --build
```

Check status of the containers.
``` bash
docker ps -a
```
It should look similar to this:
<p align="left">
    <img src="https://github.com/ohld/django-telegram-bot/raw/main/.github/imgs/containers_status.png">
</p>

Try visit <a href="http://0.0.0.0:8000/tgadmin">Django-admin panel</a>.

### Enter django shell:

``` bash
docker exec -it dtb_django bash
```

### Create superuser for Django admin panel

``` bash
python manage.py createsuperuser
```

### To see logs of the container:

``` bash
docker logs -f dtb_django
```

```


----
