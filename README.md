# Flask test app

## Переменные окружения:

**Для запуска проекта необходимо создать `.env` файл со следующими переменными окружения:**

1. Секретный ключ проекта `SECRET_KEY`, [документация](https://flask.palletsprojects.com/en/2.3.x/config/#SECRET_KEY)

2. `URI` базы данных, он же `SQLALCHEMY_DATABASE_URI`, [документация](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/)

Пример:

```sh 
postgresql://<db-user>:<db-user-password>@<db-ip-or-domain>:<port_number>/<database_name>
```

**Переменные ниже нужно просто експортировать в окружение:**

Имя flask-приложения `FLASK_APP`:

```sh 
export FLASK_APP=<app_name>
```

Настройка дебага `FLASK_DEBUG`:

```sh 
export FLASK_DEBUG=1
```

## Настройка базы данных

**В проекте используется субд `postgresql`**

1. Создание базы данных 

```sql
CREATE DATABASE <database_name>;
CREATE USER <db_user> WITH ENCRYPTED PASSWORD <passwor_for_db>;
GRANT ALL PRIVELEGES ON DATABASE <database_name> TO <db_user>;
ALTER DATABASE <database_name> OWNER TO <database_user>;
```

- Тестирование базы данных

```sh 
flask shell
```

```python 
from entry_app.models import User_
```

```python
User_.query.all()
```


## Тестирование `CRUD api`

- Абзац про получение токена

- Тестовый запрос

```sh 
curl -X POST http://127.0.0.1:5000/api/entry \
  -H 'Authorization: Bearer <token>' \
  -H 'Content-Type: application/json' \
   -d '{"text": "<some_text>"}'
```
