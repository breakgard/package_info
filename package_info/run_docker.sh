#!/bin/bash
set -e
export ES_HOME=/usr/share/elasticsearch
export ES_PATH_CONF=/etc/elasticsearch
export PID_DIR=/var/run/elasticsearch
export ES_SD_NOTIFY=true
echo "Starting elasticsearch"
chown -R elasticsearch.elasticsearch /data/elasticsearch
sudo -u elasticsearch /usr/share/elasticsearch/bin/elasticsearch -d
sleep 5

echo "Starting database"
chown -R mysql.mysql /data/mysql
mkdir /run/mysqld
chown -R mysql.mysql /run/mysqld
if [ ! -d "/data/mysql/data/mysql" ];
then
  /usr/bin/mysql_install_db --datadir=/data/mysql/data
fi
/usr/sbin/mysqld --defaults-file=/etc/mysql/my.cnf &
sleep 10
echo "Checking if database is created"
export DJANGO_DB_NAME='package_info'
export DJANGO_DB_USER='package_info'
export DJANGO_DB_PASS='package_info'
export DJANGO_DB_HOST='localhost'
set +e
DB_CREATED=$(echo 'SHOW DATABASES' | /usr/bin/mysql | grep "$DJANGO_DB_NAME")
set -e
if [ -z "$DB_CREATED"  ];
then
  echo "DB not created - creating"
  echo "CREATE DATABASE $DJANGO_DB_NAME" | /usr/bin/mysql
  echo "CREATE USER $DJANGO_DB_USER@'localhost' IDENTIFIED BY '$DJANGO_DB_PASS'" | /usr/bin/mysql
  echo "GRANT ALL PRIVILEGES ON $DJANGO_DB_NAME.* TO $DJANGO_DB_USER@'localhost'" | /usr/bin/mysql
  /app/venv/bin/python3 manage.py migrate
  /app/venv/bin/python3 manage.py search_index --rebuild -f
fi

echo "Starting background tasks"
/app/venv/bin/python3 manage.py process_tasks &
echo "Starting django"
if [ "$DJANGO_DEBUG" == 'False' ];
then
  /app/venv/bin/python3 manage.py runserver 0.0.0.0:8000 --insecure  #Fix this by icluding an actual wev server in the dockerfile
else
  /app/venv/bin/python3 manage.py runserver 0.0.0.0:8000
fi
