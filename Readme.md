# B/S 商品比价网站
## 注意
Docker 部署的方式由于浏览器问题没有办法进行爬虫相关的操作（主要为平台内搜索和历史价格搜索功能），若要进行爬虫相关的操作只能采用本地部署

# 项目结构
`./app` 项目前端
`./backend`以及`./djangoProject` 项目后端
`./data` 项目爬取的一些商品信息以及项目某些表的sql文件
`./catch` 项目爬虫文件（用于爬取信息加入数据库）
`./report` 项目报告，包括设计报告、用户使用手册、测试报告灯（设计报告部分有修改）

## 本地部署
### 数据库

1. 更改`djangoProject/settings.py`中有关数据库的设置：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # change the content to your local database information
        'NAME': 'bs', # 数据库名称，根据自己数据库的名称修改
        'USER': 'root', # 用户名
        'PASSWORD': 'Sql_201208', # 数据库对应的密码
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

代码在backend/management/commands文件夹下:

1. 为之前没有加hash_link的商品加hash_link（现在已经用不到了）
`python manage.py update_link_hash`

2. 更新用户关注的商品价格
`python manage.py update_favorite_prices`
（更新整个数据库商品价格的逻辑和更新用户关注的商品价格逻辑一样，由于数据库太大，爬虫登录困难，故没有实现）

3. 商品有降价，给用户发邮件
`python manage.py send_emails`