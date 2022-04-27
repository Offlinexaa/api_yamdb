# api_yamdb

Расширяемая база рецензий и отзывов. Предоставляет доступ через web-интерфейс и c использованием REST API

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Offlinexaa/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

```
python3 -m pip install --upgrade pip setuptools pillow
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Подготовить и выполнить миграции:

```
python3 manage.py makemigrations
```

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Документация доступна по ссылке:

```
http://127.0.0.1:8000/redoc/
```

### Требования:
Python 3.7 или выше
Django framework 2.2.16
Django Rest framework 3.12.4
