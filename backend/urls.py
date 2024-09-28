from django.urls import path
from backend import views

urlpatterns = [
    path('register', views.register),
    # http://127.0.0.1:8000/backend/register?username=ACD&email=12345@163.com&password=sf12343
    # http://127.0.0.1:8000/backend/register?username=cindy&email=zju@163.com&password=aaa111
    path('login', views.login),
    # http://127.0.0.1:8000/backend/login?email=12345@163.com&password=sf12343
]