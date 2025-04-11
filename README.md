REST API для бронирования столиков в ресторане. 
Сервис создает, вовращает и удаляет брони, управляет столиками и временными слотами.

Эндпоинты:
- GET /tables/ — список всех столиков
- POST /tables/ — создать новый столик
- DELETE /tables/{id} — удалить столик
- GET /reservations/ — список всех броней
- POST /reservations/ — создать новую бронь
- DELETE /reservations/{id} — удалить бронь

Структура основной папки проекта table_reservation:
- reserv/ - API: models, serializers, views, urls, admin и папка tests (unittest)
- table_reservation/ - конфигурация проекта
- db_data.json - данные БД для теста API

Использованные технологии:
- Django
- DRF
- PostgreSQL
- unittest
- Docker

Инструкция по запуску Docker (из папки api/):
- docker-compose up --build
- docker-compose run drf-api python manage.py migrate
- docker compose up
- docker compose exec drf-api python manage.py loaddata db_data.json
