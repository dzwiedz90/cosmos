# Cosmos app

-------------
-------------
### Technologies used:
- Python 3.8.10
- Django 4.0.6
- psycopg2-binary==2.9.3
- python-dotenv==0.20.0
- Postgres 14.2


### Configuration before first run:
- download master from repo
- configure virtual environment in Python:
    - virtualenv environment_name
    - install modules from requirements.txt (pip install -r requirements.txt)
- configure Postgres like shown in below example (you may want to use different data):
  - create database named 'cosmos', use port 5432
  - create user 'postgres' with password 'postgres'
  - add privileges to db for user postgres with:
    - GRANT ALL PRIVILEGES ON DATABASE cosmos TO postgres;
- save SECRET_KEY and db configuration:
  - create .env file in root folder where manage.py file is
  - insert data like:
```
'SECRET_KEY' = 'secret_key'
'DB_ENGINE' = 'django.db.backends.postgresql_psycopg2'
'DB_NAME' = 'db_name'
'DB_USER' = 'db_user'
'DB_PASSWORD' = 'db_password'
'DB_HOST' = 'db_host'
'DB_PORT' = 'db_port'
```
- django migrations:
  - python3 manage.py makemigrations interstellar_app
  - python3 manage.py migrate
- django create super user:
  - python3 manage.py createsuperuser
- create built in model instances:
  - python3 manage.py loaddata interstellar_app/fixtures/interstellar_object.json --app interstellar_app.InterstellarObject
  - python3 manage.py loaddata interstellar_app/fixtures/solar_system_object.json --app interstellar_app.SolarSystemObject
  - python3 manage.py loaddata interstellar_app/fixtures/moon_object.json --app interstellar_app.MoonObject
- run django server(python3 manage.py runserver)

----------------  
---------------- 