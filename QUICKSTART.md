# 🚀 Быстрый старт / Quick Start Guide

## Вариант 1: Запуск с Docker (Рекомендуется) / Option 1: Run with Docker (Recommended)

### Предварительные требования / Prerequisites
- Docker Desktop или Docker Engine
- Docker Compose

### Шаги / Steps

1. Клонируйте репозиторий:
```bash
git clone https://github.com/Steindvart/Git-Komet.git
cd Git-Komet
```

2. Запустите приложение:
```bash
docker-compose up --build
```

3. Откройте браузер:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Вариант 2: Ручная установка / Option 2: Manual Installation

### Предварительные требования / Prerequisites
- Python 3.10+
- Node.js 18+
- Git

### Backend Setup

1. Перейдите в директорию backend:
```bash
cd backend
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv

# Linux/macOS:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте окружение:
```bash
cp .env.example .env
# Отредактируйте .env если необходимо
```

5. Инициализируйте базу данных:
```bash
python init_db.py
```

6. Запустите сервер:
```bash
python run.py
```

Backend будет доступен на http://localhost:8000

### Frontend Setup

1. Откройте новый терминал и перейдите в директорию frontend:
```bash
cd frontend
```

2. Установите зависимости:
```bash
npm install
# или
yarn install
# или
pnpm install
```

3. Настройте окружение:
```bash
cp .env.example .env
# Убедитесь, что API_BASE_URL указывает на ваш backend
```

4. Запустите dev-сервер:
```bash
npm run dev
```

Frontend будет доступен на http://localhost:3000

## Первые шаги / First Steps

После запуска приложения:

1. **Добавьте репозиторий**
   - Перейдите в "Repositories"
   - Нажмите "+ Add Repository"
   - Введите имя, URL и описание
   - Нажмите "Sync Commits" для загрузки данных

2. **Создайте команду**
   - Перейдите в "Teams"
   - Нажмите "+ Add Team"
   - Введите название и описание команды
   - Добавьте участников команды

3. **Просмотрите метрики**
   - Перейдите в "Metrics"
   - Выберите команду или репозиторий
   - Просмотрите визуализации эффективности

## Тестирование / Testing

### Backend Tests
```bash
cd backend
pip install -r requirements-dev.txt
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## API Documentation

После запуска backend, документация API доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Примеры использования API / API Usage Examples

### Создание репозитория / Create Repository
```bash
curl -X POST "http://localhost:8000/api/v1/repositories" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Project",
    "url": "https://github.com/user/project.git",
    "description": "Project description"
  }'
```

### Синхронизация коммитов / Sync Commits
```bash
curl -X POST "http://localhost:8000/api/v1/repositories/1/sync"
```

### Получение метрик команды / Get Team Metrics
```bash
curl "http://localhost:8000/api/v1/metrics/team/1/effectiveness?period_days=30"
```

## Устранение проблем / Troubleshooting

### Backend не запускается
- Проверьте, что Python 3.10+ установлен: `python --version`
- Убедитесь, что все зависимости установлены: `pip list`
- Проверьте логи на наличие ошибок

### Frontend не запускается
- Проверьте, что Node.js 18+ установлен: `node --version`
- Очистите кэш: `rm -rf node_modules && npm install`
- Проверьте, что backend запущен и доступен

### Ошибки с базой данных
- Удалите файл `git_komet.db` и запустите `python init_db.py` снова
- Проверьте права доступа к директории

### Ошибки CORS
- Убедитесь, что URL frontend добавлен в `BACKEND_CORS_ORIGINS` в `backend/.env`
- Перезапустите backend после изменения настроек

## Дополнительная информация / Additional Information

Подробная документация:
- [Конфигурация / Configuration](CONFIGURATION.md)
- [Backend README](backend/README.md)
- [Frontend README](frontend/README.md)

## Поддержка / Support

Если у вас возникли проблемы:
1. Проверьте раздел Troubleshooting выше
2. Посмотрите Issues в репозитории
3. Создайте новый Issue с описанием проблемы
