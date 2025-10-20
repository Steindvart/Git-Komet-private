# Git-Komet

Система автооценки эффективности команд через анализ Git-метрик.
Team Effectiveness Analysis System Through Git Metrics.

## 📋 Описание / Description

Git-Komet - это система для анализа эффективности работы команд разработки через метрики Git-репозиториев. Проект разработан для участия в хакатоне на тему "Разработайте систему автооценки эффективности команд через анализ Git-метрик".

Git-Komet is a system for analyzing development team effectiveness through Git repository metrics. The project is developed for a hackathon on the theme "Develop a system for automatic team effectiveness evaluation through Git metrics analysis".

## 🚀 Стек технологий / Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Современный, быстрый веб-фреймворк для создания API
- **SQLAlchemy** - ORM для работы с базой данных
- **SQLite** - Легковесная база данных для хранения метрик
- **GitPython** - Библиотека для взаимодействия с Git-репозиториями
- **Pandas/NumPy** - Анализ и обработка данных

### Frontend
- **Vue.js 3** - Прогрессивный JavaScript-фреймворк
- **Nuxt.js 3** - Фреймворк для Vue.js приложений
- **TypeScript** - Типизированный JavaScript
- **Nuxt UI** - Библиотека UI компонентов
- **Chart.js + vue-chartjs** - Визуализация данных и построение графиков

## 📁 Структура проекта / Project Structure

```
Git-Komet/
├── backend/                  # Backend API (Python + FastAPI)
│   ├── app/
│   │   ├── api/             # API endpoints
│   │   │   └── endpoints/   # Route handlers
│   │   ├── core/            # Core configuration
│   │   ├── db/              # Database configuration
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── main.py         # FastAPI application
│   ├── tests/               # Tests
│   ├── requirements.txt     # Python dependencies
│   ├── .env.example        # Environment variables example
│   ├── init_db.py          # Database initialization
│   ├── run.py              # Application runner
│   └── README.md           # Backend documentation
│
├── frontend/                # Frontend (Vue.js + Nuxt.js)
│   ├── assets/             # Static assets (CSS, images)
│   ├── components/         # Vue components
│   ├── composables/        # Composable functions
│   ├── layouts/            # Page layouts
│   ├── pages/              # Application pages
│   ├── plugins/            # Nuxt plugins
│   ├── public/             # Public static files
│   ├── nuxt.config.ts     # Nuxt configuration
│   ├── package.json        # Node dependencies
│   └── README.md          # Frontend documentation
│
├── .gitignore              # Git ignore rules
└── README.md              # This file
```

## 🔧 Установка и запуск / Installation & Setup

### Backend Setup

1. Перейдите в директорию backend:
```bash
cd backend
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Скопируйте файл окружения:
```bash
cp .env.example .env
```

5. Инициализируйте базу данных:
```bash
python init_db.py
```

6. Запустите сервер:
```bash
python run.py
```

Backend API будет доступен по адресу: http://localhost:8000

### Frontend Setup

1. Перейдите в директорию frontend:
```bash
cd frontend
```

2. Установите зависимости:
```bash
npm install
# или
yarn install
```

3. Создайте файл .env:
```bash
echo "API_BASE_URL=http://localhost:8000/api/v1" > .env
```

4. Запустите dev-сервер:
```bash
npm run dev
```

Frontend будет доступен по адресу: http://localhost:3000

## 📊 Возможности / Features

### Основные функции / Main Features

- ✅ **Управление репозиториями** - Добавление и синхронизация Git-репозиториев
- ✅ **Управление командами** - Создание команд и добавление участников
- ✅ **Анализ коммитов** - Сбор и анализ метрик коммитов
- ✅ **Метрики эффективности** - Расчет показателей эффективности команд
- ✅ **Визуализация данных** - Графики и дашборды для отображения метрик
- ✅ **RESTful API** - Полноценный API для интеграции

### Анализируемые метрики / Analyzed Metrics

- 📈 **Частота коммитов** (Commit Frequency)
- 📊 **Изменения кода** (Code Churn)
- 👥 **Активные участники** (Active Contributors)
- 📝 **Размер коммитов** (Commit Size)
- ⏱️ **Временные паттерны** (Time Patterns)

## 📖 API Documentation

После запуска backend сервера, документация API доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🧪 Тестирование / Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 🤝 Участие в разработке / Contributing

Этот проект создан для хакатона. Для участия в разработке:

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/AmazingFeature`)
3. Зафиксируйте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Отправьте изменения (`git push origin feature/AmazingFeature`)
5. Создайте Pull Request

## 📝 Лицензия / License

Проект создан для хакатона и образовательных целей.

## 👨‍💻 Авторы / Authors

Разработано для хакатона на тему "Разработайте систему автооценки эффективности команд через анализ Git-метрик".

## 🎯 Цели проекта / Project Goals

1. Автоматизация оценки эффективности команд разработки
2. Визуализация метрик производительности
3. Выявление паттернов и трендов в работе команды
4. Предоставление данных для принятия управленческих решений

## 📧 Контакты / Contact

Для вопросов и предложений создайте Issue в репозитории.