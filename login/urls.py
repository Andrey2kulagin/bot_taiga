from django.urls import path
from .views import classic_login, application_login
urlpatterns = [
    path('standard', classic_login, name="standard_login"),
    path('application', application_login, name="application_login")
]
