from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.sites.models import Site
def generate_standard_auth_link(domain, tg_id):
    link = reverse("standard_login")
    
    absolute_url = get_link_with_basic_domain(link)
    return append_query_to_link(absolute_url, domain, tg_id)
def get_link_with_basic_domain(link):
    """_summary_
    Приклеивает эндпоинт к домену нашего сайта(задачется в админке)
    """
    current_site = get_current_site(None)
    current_site = Site.objects.get_current()
    # Построение абсолютного URL с использованием протокола, домена и относительного пути
    return f'{current_site.domain}{link}'

def generate_application_auth_link(domain, tg_id):
    link = reverse("application_login")
    absolute_url = get_link_with_basic_domain(link)
    return append_query_to_link(absolute_url, domain, tg_id)

def append_query_to_link(link, domain, tg_id):
    """_summary_
    Добавляет аргументы в ссылку
    """
    return f"{link}?domain={domain}&tg_id={tg_id}"