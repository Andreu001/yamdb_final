# CI и CD проекта api_yamdb

## Используемые технологии:
![Django-app workflow](https://github.com/RoiAlexandr/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=56C0C0&color=008080)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=56C0C0&color=008080)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat&logo=Django%20REST%20Framework&logoColor=56C0C0&color=008080)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat&logo=PostgreSQL&logoColor=56C0C0&color=008080)](https://www.postgresql.org/)
[![JWT](https://img.shields.io/badge/-JWT-464646?style=flat&color=008080)](https://jwt.io/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat&logo=NGINX&logoColor=56C0C0&color=008080)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat&logo=gunicorn&logoColor=56C0C0&color=008080)](https://gunicorn.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker-compose](https://img.shields.io/badge/-Docker%20compose-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/)
[![Docker Hub](https://img.shields.io/badge/-Docker%20Hub-464646?style=flat&logo=Docker&logoColor=56C0C0&color=008080)](https://www.docker.com/products/docker-hub)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat&logo=GitHub%20actions&logoColor=56C0C0&color=008080)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat&logo=Yandex.Cloud&logoColor=56C0C0&color=008080)](https://cloud.yandex.ru/)

# CI/CD для проекта API YAMDB 
Проект YaMDb собирает отзывы (Review) пользователей на произведения (Title).<br>  
Произведения делятся на категории: "Книги", "Фильмы", "Музыка". Список категорий (Category) может быть расширен.<br>  
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.<br>  
В каждой категории есть произведения: книги, фильмы или музыка. Произведению может быть присвоен жанр из списка предустановленных.<br>  
Новые жанры может создавать только администратор.<br>  
Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (Review) и выставляют произведению рейтинг.<br>  

## Ресурсы API YaMDb<br>  
**auth**: аутентификация.<br>  
  
**users**: пользователи.<br>  
  
**titles**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).<br>  
  
**categories**: категории (типы) произведений ("Фильмы", "Книги", "Музыка").<br>  
  
**genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.<br>  
  
**reviews**: отзывы на произведения. Отзыв привязан к определённому произведению.<br>  
  
**comments**: комментарии к отзывам. Комментарий привязан к определённому отзыву.<br>  
  
## Алгоритм регистрации пользователей<br>  
Пользователь отправляет POST-запрос с параметрами email и username на `/api/v1/auth/signup/`.<br>  
Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указанный адрес email.<br>  
Пользователь отправляет POST-запрос с параметрами username и confirmation_code на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит token (JWT-токен)<br>  
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле<br>  
  
## Пользовательские роли<br>  
**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.<br>  
  
**Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений.<br>  
  
**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.<br>  
  
**Администратор (admin)** — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.<br>  
 
**Суперюзер Django** — те же права, что и у роли Администратор.<br>  
  
## Workflow
* tests - Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest. Дальнейшие шаги выполнятся только если push был в ветку master или main.
* build_and_push_to_docker_hub - Сборка и доставка докер-образов на Docker Hub
* deploy - Автоматический деплой проекта на боевой сервер. Выполняется копирование файлов из репозитория на сервер:
* send_message - Отправка уведомления в Telegram

### Подготовка для запуска workflow
Создайте и активируйте виртуальное окружение, обновите pip:
```
python3 -m venv venv
. venv/bin/activate
python3 -m pip install --upgrade pip
```
Запустите автотесты:
```
pytest
```
Отредактируйте файл `nginx/default.conf` и в строке `server_name` впишите IP виртуальной машины (сервера).  
Скопируйте подготовленные файлы `docker-compose.yaml` и `nginx/default.conf` из вашего проекта на сервер:
```
scp docker-compose.yaml <username>@<host>/home/<username>/docker-compose.yaml
sudo mkdir nginx
scp default.conf <username>@<host>/home/<username>/nginx/default.conf
```
В репозитории на Гитхабе добавьте данные в `Settings - Secrets - Actions secrets`:
```
DOCKER_USERNAME - имя пользователя в DockerHub
DOCKER_PASSWORD - пароль пользователя в DockerHub
HOST - ip-адрес сервера
USER - пользователь
SSH_KEY - приватный ssh-ключ (публичный должен быть на сервере)
PASSPHRASE - кодовая фраза для ssh-ключа
DB_ENGINE - django.db.backends.postgresql
DB_NAME - postgres (по умолчанию)
POSTGRES_USER - postgres (по умолчанию)
POSTGRES_PASSWORD - postgres (по умолчанию)
DB_HOST - db
DB_PORT - 5432
SECRET_KEY - секретный ключ приложения django (необходимо чтобы были экранированы или отсутствовали скобки)
ALLOWED_HOSTS - список разрешённых адресов
TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)
```
При внесении любых изменений в проект, после коммита и пуша
```
git add .
git commit -m "комит"
git push
```
запускается набор блоков команд jobs (см. файл yamdb_workflow.yaml), т.к. команда `git push` является триггером workflow проекта.

## Как развернуть проект локально:
 ***Склонируйте репозиторий***:
``` bash
git clone git@github.com:RoiAlexandr/yamdb_final.git  
```
***Создайте виртуальное окружение и активируйте его***: 
python -m venv venv
``` bash
Windows: source venv\scripts\activate
Linux/Mac: source venv/bin/activate
``` 
***Обновите pip и установите зависимости***:
``` bash
python -m pip install -r requirements.txt  
python -m pip install --upgrade pip
```
  
Для запуска остальных команд перейдите в каталог api_yamdb 
```bash
cd api_yamdb
```
Запустите миграции
```
python manage.py migrate 
```
Загрузите тестовые данные из csv файлов 
```
python manage.py parser_csv
```
Создайте суперпользователя
```
python manage.py createsuperuser
```
Запустите сервер 
```
python manage.py runserver  
```
  
  
Проект запущен и доступен по адресу [localhost:8000](http://localhost:8000/)
  
Документация API YaMDb доступна по адресу [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

## Развёрнутый проект
http://51.250.1.54/api/v1/
http://51.250.1.54/admin/
http://51.250.1.54/redoc/

## Примеры запросов и ответов

- *api/v1/signup/* - регистрация нового пользователя
```json
{
  "email": "string",
  "username": "string"
}
```
- *api/v1/token/* - получить токен (используйте код из почты)
```json
{
  "username": "string",
  "confirmation_code": "string"
}
```
- *api/v1/categories/* - категории произведений
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
- *api/v1/genres/* - Жанры произведений
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
- *api/v1/titles/* - Произведения
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "name": "string",
        "year": 0,
        "rating": 0,
        "description": "string",
        "genre": [
          {
            "name": "string",
            "slug": "string"
          }
        ],
        "category": {
          "name": "string",
          "slug": "string"
        }
      }
    ]
  }
]
```
- *api/v1/titles/{title_id}/reviews/* - Отзывы на произведения
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2022-06-29T18:15:22Z"
      }
    ]
  }
]
```
- *api/v1/titles/{title_id}/reviews/{rewiew_id}/comments/* - Комментарии к отзывам
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2022-06-29T18:15:22Z"
      }
    ]
  }
]
```
- *api/v1/users/* - Управление пользователями
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```
- *api/v1/users/me/* - Управление своей учетной записью
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
