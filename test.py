from django.core.mail import send_mail
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')  # 替换'myproject'为你的项目名称
django.setup()
send_mail(
    'Test Subject',
    'Test message',
    'CindyZhou6418@gmail.com',
    ['Cindyzhou2003@outlook.com'],
    fail_silently=False,
)
