# Конфигурация проекта / Project Configuration

## Переменные окружения Backend / Backend Environment Variables

Создайте файл `backend/.env` на основе `backend/.env.example`:

```bash
# Database
DATABASE_URL=sqlite:///./git_komet.db

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=Git-Komet
DEBUG=True

# CORS - добавьте URL вашего фронтенда
BACKEND_CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000"]

# Git Configuration
DEFAULT_BRANCH=main
```

### Описание переменных Backend:

- `DATABASE_URL`: URL подключения к базе данных (SQLite по умолчанию)
- `API_V1_STR`: Префикс для API endpoints
- `PROJECT_NAME`: Название проекта
- `DEBUG`: Режим отладки (True для разработки)
- `BACKEND_CORS_ORIGINS`: Список разрешенных origins для CORS
- `DEFAULT_BRANCH`: Ветка по умолчанию для анализа Git

## Переменные окружения Frontend / Frontend Environment Variables

Создайте файл `frontend/.env` на основе `frontend/.env.example`:

```bash
# API Configuration
API_BASE_URL=http://localhost:8000/api/v1
```

### Описание переменных Frontend:

- `API_BASE_URL`: Базовый URL для подключения к backend API

## Docker Configuration

Если используете Docker Compose, можно настроить переменные в `docker-compose.yml`

## Порты / Ports

По умолчанию используются следующие порты:

- Backend API: `8000`
- Frontend: `3000`

Если нужны другие порты, измените их в:
- Backend: `backend/run.py` и `backend/Dockerfile`
- Frontend: `docker-compose.yml` и команда запуска

## База данных / Database

По умолчанию используется SQLite. Файл базы данных создается в `backend/git_komet.db`

Для использования другой базы данных:
1. Установите соответствующий драйвер в `requirements.txt`
2. Измените `DATABASE_URL` в `.env`

Пример для PostgreSQL:
```
DATABASE_URL=postgresql://user:password@localhost:5432/git_komet
```

## Git Authentication

Если репозитории требуют аутентификации:

1. Используйте SSH URL вместо HTTPS
2. Настройте SSH ключи на сервере
3. Или используйте Personal Access Token в URL:
   ```
   https://token@github.com/user/repo.git
   ```

## Production Configuration

Для production окружения:

1. Установите `DEBUG=False`
2. Используйте надежную базу данных (PostgreSQL, MySQL)
3. Настройте HTTPS
4. Используйте gunicorn для backend:
   ```bash
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```
5. Соберите frontend для production:
   ```bash
   npm run build
   npm run start
   ```

## Troubleshooting

### Backend не запускается

1. Проверьте, что установлены все зависимости: `pip install -r requirements.txt`
2. Проверьте, что инициализирована база данных: `python init_db.py`
3. Проверьте права доступа к файлу базы данных

### Frontend не подключается к Backend

1. Проверьте, что Backend запущен и доступен
2. Проверьте `API_BASE_URL` в `frontend/.env`
3. Проверьте CORS настройки в `backend/.env`

### Ошибки с Git репозиториями

1. Убедитесь, что Git установлен на сервере
2. Проверьте права доступа к репозиториям
3. Для приватных репозиториев настройте аутентификацию
