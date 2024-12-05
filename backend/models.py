from datetime import datetime
from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)  # 使用set_password来加密密码
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=45, unique=True)
    email = models.EmailField(max_length=45, unique=True)
    password = models.CharField(max_length=128, null=False)
    email_active = models.BooleanField(default=True) # 邮件提醒 默认开
    is_admin = models.BooleanField(default=False)

    objects = MyAccountManager()

    # Change this field to use `email` for login
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def change_email_state(self,state):
        self.email_active = state
        self.save()


class Products(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null=False)  # 商品名称
    price = models.FloatField(null=False)  # 商品当前价格
    info = models.CharField(max_length=50, null=False)  # 评论数或购买人数
    shop = models.CharField(max_length=50, null=False)  # 店铺名
    img = models.CharField(max_length=350, null=False)  # 商品图片 URL
    link = models.CharField(max_length=300, unique=True, null=False)  # 商品购买链接
    platform = models.CharField(max_length=20, null=False)  # 电商平台

    def __str__(self):
        return self.title

    def modify_price(self,new_price):
        """更新价格"""
        self.price = new_price
        self.save()


class Prices(models.Model): # 商品历史价格表
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, related_name='prices', on_delete=models.CASCADE)  # 外键关联到 Products
    price = models.FloatField(null=False)  # 商品历史价格
    is_valid = models.BooleanField(default=True)  # 价格是否有效
    created_at = models.DateTimeField(auto_now_add=True)  # 价格记录创建时间

    def __str__(self):
        return f"{self.product.title} - ￥{self.price} on {self.platform}"

    class Meta:
        ordering = ['-created_at']  # 默认按创建时间降序排列


class Likes(models.Model): # 用户关注的商品列表
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(Account, related_name='likes', on_delete=models.CASCADE)  # Link to Account
    product = models.ForeignKey(Products, related_name='liked_by', on_delete=models.CASCADE)  # Link to Products
    created_at = models.DateTimeField(auto_now_add=True) # 关注商品时间
    def __str__(self):
        return f"{self.product.title} liked by {self.user_id} on {self.created_at}"

    class Meta:
        unique_together = ('user_id', 'product')  # Ensure a user can like a product only once