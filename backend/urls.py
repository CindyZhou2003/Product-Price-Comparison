from django.urls import path
from backend import views

urlpatterns = [

    path('register', views.register),# 注册
    path('login', views.login), # 登录

    path('change_password', views.change_password), # 修改密码
    path('reset_password', views.reset_password), # 通过邮箱重置密码
    path('reset_email', views.reset_email),# 通过密码重置邮箱
    path('send_verification_code', views.send_verification_code), # 发送验证码
    path('verify_code', views.verify_code), # 检验验证码

    path('search_products', views.search_products), # 搜索数据库中商品
    path('search_through_categories', views.search_through_categories), # 根据分类搜索商品
    path('get_categories', views.get_categories), # 得到分类树
    path('update_and_show_price', views.update_and_show_price), # 更新单个商品价格
    path('show_price', views.show_price),

    path('like', views.like), # 关注商品
    path('unlike', views.unlike), # 取消关注
    path('get_favorites', views.get_favorites), # 展示关注列表

    path('search_platform_products', views.search_platform_products), # 平台搜索（爬虫）商品加入数据库
    path('send_user_email', views.send_user_email), # 发送降价邮件提醒

    path('change_email_service_state', views.change_email_service_state), # 用户是否想要发送降价提醒
    path('get_user_info', views.get_user_info), # 获取用户名
]