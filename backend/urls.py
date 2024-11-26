from django.urls import path
from backend import views

urlpatterns = [
# http://127.0.0.1:8000/backend/register?username=ACD&email=12345@163.com&password=sf12343
# http://127.0.0.1:8000/backend/login?email=12345@163.com&password=sf12343
    path('register', views.register),# 注册
    path('login', views.login), # 登录
    path('change_password', views.change_password), # 修改密码

    path('get_all_products',views.get_all_products), # 展示数据库所有商品
    path('search_products', views.search_products), # 搜索数据库中商品
    path('update_and_show_price',views.update_and_show_price), # 更新单个商品价格

    path('like', views.like), # 关注商品
    path('unlike',views.unlike), # 取消关注
    path('get_favorites',views.get_favorites), # 展示关注列表

    path('search_platform_products',views.search_platform_products), # 平台搜索（爬虫）商品加入数据库
    path('send_user_email',views.send_user_email), # 发送降价邮件提醒

]