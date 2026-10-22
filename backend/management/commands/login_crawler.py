from django.core.management.base import BaseCommand
from backend.crawler import login_crawler


class Command(BaseCommand):
    help = "Open a browser to log in to Taobao/JD manually and keep the login for the crawler."

    def add_arguments(self, parser):
        parser.add_argument('platform', choices=['taobao', 'jd'])

    def handle(self, *args, platform, **kwargs):
        login_crawler(platform)
        self.stdout.write("登录状态已保存")
