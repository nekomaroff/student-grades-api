# Student Grades API

REST API для загрузки и анализа оценок студентов.

## Возможности

- Загрузка оценок студентов из CSV-файла
- Сохранение данных в PostgreSQL
- Получение статистики по количеству оценок «2» у студентов
- Проверка состояния сервиса (healthcheck)
- Полностью контейнеризированный запуск (API + БД)

## Архитектура проекта

Проект разделён на логические слои:
app/
- routes.py # HTTP-эндпоинты (FastAPI)
- services/grades_service.py # Бизнес-логика
- repositories/grades_repository.py # Работа с базой данных (SQL)
- schemas/grades.py # Pydantic-схемы (request / response)
- tests/test_api.py # Автотесты (pytest)
- db.py # Подключение к БД и execute_query
- constants.py # Константы и конфигурация
- main.py # Инициализация FastAPI-приложения
- routes.py

Такое разделение упрощает поддержку кода и соответствует базовым принципам SOLID и чистой архитектуры.

## Конфигурация

DB_HOST=postgres
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=grades

## Запуск проекта (Docker Compose)
docker-compose up --build

После запуска:
- API будет доступно на http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- База данных PostgreSQL поднимается автоматически
- API стартует только после готовности БД (через healthcheck

Остановка и очистка данных: docker-compose down -v

## Запуск тестов
Для запуска тестов используется pytest - в проекте реализован базовый API-тест, проверяющий доступность сервиса

## Формат CSV-файла
Загружаемый CSV-файл должен иметь следующий формат: 
Дата - 01.09.2024
Номер группы - 101
ФИО - Иванов И.И.
Оценка - 5

Поддерживаемые оценки: 2, 3, 4, 5

## API-эндпоинты

POST /upload-grades

Загрузка CSV-файла с оценками студентов

GET /students/more-than-3-twos

Получить студентов с более чем 3 оценками «2»

GET /students/less-than-5-twos

Получить студентов с менее чем 5 оценками «2»

GET /healthcheck

## База данных
Структура базы данных создаётся автоматически при старте контейнера.

SQL-скрипт находится в файле: sql/init.

## Используемые технологии

- Python 3.11
- FastAPI
- PostgreSQL
- psycopg2
- Docker / Docker Compose
- pytest