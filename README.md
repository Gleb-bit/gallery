# GALLERY

# Запуск с использованием Docker:

## Создание контейнера docker:

* ```docker-compose -f docker-compose.yml build```

## Поднятие контейнера docker:

* ```docker-compose -f docker-compose.yml up```

## Удаление всех контейнеров и образов docker:

* ```docker rm $(docker ps -a -q) -f;docker rmi $(docker images -q) -f```

# Запуск на локальной машине:

## Установка сторонних зависимостей:

* ```pip install -r requirements.txt```

## Создание миграций:

* ```python manage.py makemigrations```

## Применение миграций:

* ```python manage.py migrate```

## Запуск сервера:

* ```python manage.py runserver```
