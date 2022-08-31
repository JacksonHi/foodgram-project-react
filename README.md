# Проект foodgram

```
Проект foodgram предназначен для публикации рецептов. Здесь вы можете зарегистрироваться, чтобы создать свои рецепты, подписаться на других пользователей, добавить рецепты в избранные, добавить ингредиенты в корзину и в дальнейшем скачать их текстовым файлом.
```

## Информоция для ревьюера:
- ip 84.201.166.53
- Админка admin admin

## Технологии:
- Python 3.10
- Django 4.0.5
- Django REST framework 3.13.1
- djoser 2.1.0
- python-dotenv 0.20.0
- gunicorn 20.1.0
- psycopg2-binary 2.9.3

## Начало работы
скопировать репозиторий:
```
git clone <адрес репозитория>
```
создать и развернуть виртуальное окружение:
```
python3 -m venv venv
```
```
. venv/bin/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```
Создайте .env файл в корне репозитория и заполните его
Поля для заполнения и примеры:
```
SECRET_KEY=123

DB_ENGINE=django.db.backends.postgresql

DB_NAME=foodgram

POSTGRES_USER=user

POSTGRES_PASSWORD=xxxyyyzzz

DB_HOST=db

DB_PORT=5432
```

## Создание образа для DockerHub
Перейдите к файлу backend/foodgram/Dockerfile и frontend/Dockerfile
Локально создать образ с нужным названием и тегом:
```
docker build -t user_name/name_file:v31.08.2022 .
```
Авторизоваться через консоль:
```
docker login
```
Загрузить образ на DockerHub:
```
docker push user_name/name_file:v31.08.2022 
```

## Подготовка удаленного сервера
Для работы с проектом на удаленном сервере должен быть установлен Docker и docker compose.
Установите docker:
```
sudo apt install docker.io 
```
Установите docker-compose, с этим вам поможет официальная документация:
```
https://docs.docker.com/compose/install/
```
При помощи утилиты scp
```
$ scp опции файл пользователь@хост:файл
```
Скопируйте файлы infra/docker-compose.yaml и infra/nginx.conf из проекта на сервер в home/<ваш_username>/infra/docker-compose.yaml и home/<ваш_username>/infra/nginx.conf
Скопируйте подготовленные данные для заполнения балы данных data/tag.json и data/new_ingredients.json из проекта на сервер в home/<ваш_username>/data/tag.json и home/<ваш_username>/data/new_ingredients.json

## Развертывание приложения
Подлкючитесь к серверу:
```
ssh <USER>@<HOST>
```
Перейдите в директорию с файлом docker-compose.yaml и запустите сбор контейнеров:
```
docker compose up
```
При помощи 'docker cp' скопируйте подготовленные данные для заполнения балы данных home/<ваш_username>/data/tag.json и home/<ваш_username>/data/new_ingredients.json из сервера в контейнер app/tag.json и app/new_ingredients.json

Перейдите в запущенный контейнер backend приложения командой:
```
docker exec -it <CONTAINER ID> bash
```
Внутри контейнера необходимо провести миграции, собрать статику приложения, создать суперпользователя и загрузить данные в базу:
```
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py createsuperuser
python manage.py loaddata tag.json new_ingredients.json
```

## Адреса для взаимодействия
Админка:
```
http://178.154.193.163/admin/
```
Сайт:
```
http://178.154.193.163/api/v1/
```
