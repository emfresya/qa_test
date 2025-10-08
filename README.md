# Система мониторинга ресурсов

## Описание

Django-приложение для мониторинга ресурсов удалённых машин с автоматическим сбором метрик, фиксацией инцидентов и веб-интерфейсом для просмотра событий. Архитектура масштабируема, поддерживает запуск через Docker Compose и локально.

## Основные возможности
- Периодический опрос HTTP-эндпоинтов 30 машин (mock-сервер для теста)
- Сохранение метрик в MySQL
- Фоновая обработка задач через Celery
- Фиксация инцидентов при превышении порогов
- Веб-интерфейс для просмотра инцидентов
- Аутентификация через собственный middleware

## Запуск через Docker Compose

1. Убедитесь, что установлен Docker и Docker Compose.
2. Скопируйте `.env` из примера или настройте свои переменные (секреты, доступы к БД).
3. Запустите:
   ```bash
   docker-compose up --build
   ```
4. Django будет доступен на http://localhost:8000
5. Mock-сервер для теста метрик — http://localhost:8001

## Локальный запуск (без Docker)

1. Установите Python 3.12, MySQL 8, Redis.
2. Создайте и активируйте виртуальное окружение:
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```
3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
4. Настройте `.env` (см. пример).
5. Примените миграции:
   ```bash
   python manage.py migrate
   ```
6. Запустите сервер:
   ```bash
   python manage.py runserver
   ```
7. (Опционально) Сгенерируйте тестовые данные:
   ```bash
   python create_initial_data.py
   ```
8. Запустите Celery worker и beat:
   ```bash
   celery -A monitoring_systems worker --loglevel=info
   celery -A monitoring_systems beat --loglevel=info
   ```

## Структура проекта
- monitoring_systems/ — конфигурация Django, Celery, настройки
- monitoring/ — бизнес-логика, задачи, модели метрик и инцидентов
- authentication/ — собственная аутентификация и middleware
- frontend/ — шаблоны и JS для интерфейса
- api/ — REST-API
- mock_server.py — заглушка для теста сбора метрик
- requirements.txt — зависимости
- docker-compose.yml, Dockerfile — контейнеризация
- create_initial_data.py — генерация тестовых данных (машины, метрики, инциденты)
## Переменные окружения (.env)
- SECRET_KEY — секретный ключ Django
- DEBUG — режим отладки
- MYSQL_HOST, MYSQL_PORT, MYSQL_DB, MYSQL_USER, MYSQL_PASSWORD — настройки MySQL
- REDIS_HOST, REDIS_PORT — настройки Redis


### Примеры эндпоинтов
- `/api/incidents/` — список инцидентов (GET), создание инцидента (POST)
- `/api/metrics/` — список метрик (GET)
- `/` — главная страница
- `/login/` — страница входа
- `/dashboard/` — инциденты

## Генерация тестовых данных
Для быстрого наполнения базы тестовыми машинами, метриками и инцидентами используйте:

```bash
python create_initial_data.py
```
Скрипт автоматически создаст 30 машин и сгенерирует для них метрики и инциденты для демонстрации работы системы.

## Тестирование
- Для теста сбора метрик используйте mock_server.py
- Запустите mock-сервер:
   ```bash
   python mock_server.py
   ```
- Проверьте, что метрики сохраняются и инциденты фиксируются


## Авторы
- emfresya