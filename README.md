![Build Status](https://github.com/xxxxJavaCoderxxxx/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)
### Описание:
Проект реализован с помощью Rest Framework API и предзначен для
создания отзывов (Review) на произведение (Title), соответствующео жанра (Genre) и категории (Category).
Проект предусматривает регистрацию пользователей по username и email.
Пользователь имеет право создавать отзыв на произвдение, комментировать отзывы (Comment), 
редактировать данные о себе.
### Как запустить этот чудесный проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:xxxxJavaCoderxxxx/yamdb_final.git
```

```
cd ./api_yamdb_final/infra
```
### Создать файл перменных env:
```
touch .env
```

```
DB_ENGINE=django.db.backends.postgresql 
```

```
DB_NAME= имя БД
```

```
POSTGRES_USER= Пользователь Postgres
```

```
POSTGRES_PASSWORD= Пароль от Postgres
```

```
DB_HOST= БД
```

```
DB_PORT= порт службы БД
```

### Docker:
```
docker-compose up -d --build
```
### Примеры использования API:
|:--------:|--------------:|----------------:|-----------------:|
|POST | http://127.0.0.1:8000/api/v1/auth/signup/ | {<br>"username": "string",<br>"email": "user@example.com"<br>}  | Зарегистрироваться |
|POST | http://127.0.0.1:8000/api/v1/auth/token/  |{<br>"username": "string",<br>"confirmation_code": "string"<br>} | Получить токен.    |
|PATCH| http://127.0.0.1:8000/api/v1/users/me     | {<br>"username": "string",<br>"email": "user@example.com",<br>"first_name": "string",<br>"last_name": "string",<br>"bio": "string",<br>"role": "user"<br>} |Отредактировать данные о себе|