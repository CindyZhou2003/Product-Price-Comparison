# B/S 商品比价网站
## 注意
Docker 部署的方式没有办法进行爬虫相关的操作，若要进行爬虫相关的操作需要在本地运行

## 本地部署
### 数据库

1. 更改`djangoProject/settings.py`中有关数据库的设置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # change the content to your local database information
        'NAME': 'bs', # 数据库名称
        'USER': 'root', # user
        'PASSWORD': 'Sql_201208', # 对应的密码
        # 'HOST': 'db', # docker用这个
        'HOST': 'localhost', #本地部署就是这个不用改
        # 'PORT': '3306', # docker用这个
        'PORT':'1024', #本地部署的端口（根据MySQL安装时的设置来，本人运行在1024
    }
}
```

2. 在项目根目录运行以下命令：
`python manage.py makemigrations`
`python manage.py migrate`

3. 项目根目录有一个bs.sql文件是本项目当前数据库的内容，你可以使用命令`mysql -u [username] -p bs < bs.sql`将数据一键导入数据库中
    您需要输入密码，并确保目标数据库 bs 存在。如果不存在，可以先创建： `CREATE DATABASE bs;`


## 运行
### 开启后端
在项目根目录运行以下命令
`python manage.py runserver`

### 开启前端
进入目录app，运行`npm start`
`cd app`
`npm start`

## Docker 部署
在项目根目录分别运行
`docker compose build`
`docker-compose up`

## 环境
Python 3.10 虚拟环境`.venv`
所需要的安装包和版本号在`requirements.txt`中

## 网站使用方式
### 用户

详见用户使用手册部分

### 管理员

代码在backend/management/commands文件夹下

1. 为之前没有加hash_link的商品加hash_link（现在已经用不到了）
`python manage.py update_link_hash`
2. 商品有降价，给用户发邮件
`python manage.py send_emails`
3. 更新用户关注的商品价格
`python manage.py update_favorite_prices`


