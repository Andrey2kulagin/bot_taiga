


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
