React + Django 项目结构（数据库MySQL）

- .venv（虚拟环境）

- app
  - public目录
  - src目录
  - node_modules目录
  - build目录
  - 其他文件省略
- backend
  - __init__.py
  - models.py
  - urls.py
  - view.py
  - 其他文件省略
- djangoProject
  - init.py
  - settings.py
  - urls.py
  - 其他文件省略
- manage.py
- .gitignore
- .package-lock.json

 

```

docker run --name mysql -p 1025:1024 -e MYSQL_ROOT_PASSWORD=Sql_201208 -d mysql

ALTER USER 'root'@'localhost' IDENTIFIED BY 'Sql_201208';


CREATE USER 'user'@'%' IDENTIFIED WITH mysql_native_password BY 'Sql_201208';
GRANT ALL PRIVILEGES ON *.* TO 'Sql_201208'@'%';

docker exec -it mysql bash

mysqldump -u root -p -P 1024 bs > bs_backup.sql

docker cp pcb_backup.sql <container_name>:/pcb_backup.sql

docker exec -it <container_name> mysql -u root -p pcb < /pcb_backup.sql

docker exec -it price_comparison_website-backend-1 /bin/bash


apt-get update && apt-get install -y dbus
mkdir -p /run/dbus
dbus-daemon --system --fork

docker-compose down -v #移除挂载的卷


```

Django后端的settings.py中有数据库相关的内容可能需要更改：

