from django.urls import path
from backend import views

urlpatterns = [
    path('register', views.register),
    # http://127.0.0.1:8000/backend/register?username=ACD&email=12345@163.com&password=sf12343
    path('login', views.login),
    # http://127.0.0.1:8000/backend/login?email=12345@163.com&password=sf12343
    path('search_products', views.search_products),
    # http://127.0.0.1:8000/backend/search_products?search=手机
    path('update_and_show_price',views.update_and_show_price),
]