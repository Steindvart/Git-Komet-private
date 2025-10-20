# Git-Komet

Система автооценки эффективности команд через анализ Git-метрик.
Team Effectiveness Analysis System Through Git Metrics from T1 Сфера.Код.

## 📋 Описание / Description

Git-Komet - это система для анализа эффективности работы команд разработки через метрики из T1 Сфера.Код. Проект разработан для участия в хакатоне на тему "Разработайте систему автооценки эффективности команд через анализ Git-метрик".

Git-Komet is a system for analyzing development team effectiveness through metrics from T1 Сфера.Код (Sphere.Code). The project is developed for a hackathon on the theme "Develop a system for automatic team effectiveness evaluation through Git metrics analysis".

### Интеграция с T1 Сфера.Код / T1 Sphere.Code Integration

Система интегрируется с T1 Сфера.Код и собирает данные о:
- Коммитах (commits)
- Pull Request'ах
- Code Review
- Задачах (tasks/issues)

The system integrates with T1 Sphere.Code and collects data about:
- Commits
- Pull Requests
- Code Reviews  
- Tasks/Issues

## 🚀 Стек технологий / Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Современный, быстрый веб-фреймворк для создания API
- **SQLAlchemy** - ORM для работы с базой данных
- **SQLite** - Легковесная база данных для хранения метрик
- **Pandas/NumPy** - Анализ и обработка данных
- **Mock T1 API** - Заглушка для симуляции данных из T1 Сфера.Код

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
│   │   │   ├── team_effectiveness_service.py
│   │   │   ├── technical_debt_service.py
│   │   │   ├── bottleneck_service.py
│   │   │   └── t1_mock_service.py
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

- ✅ **Интеграция с T1 Сфера.Код** - Получение данных из T1 API (с mock-данными)
- ✅ **Управление командами** - Создание команд и добавление участников
- ✅ **Анализ эффективности команд** - Комплексная оценка производительности (0-100)
- ✅ **Анализ технического долга** - Отслеживание покрытия тестами, TODO, качества ревью
- ✅ **Анализ узких мест** - Выявление bottleneck'ов в workflow (review, development, testing)
- ✅ **Визуализация данных** - Графики и дашборды для отображения метрик
- ✅ **Алерты и рекомендации** - Автоматические уведомления о проблемах
- ✅ **Тренды** - Отслеживание изменений метрик во времени
- ✅ **RESTful API** - Полноценный API для интеграции

### Анализируемые метрики / Analyzed Metrics

#### 1. Team Effectiveness Score (Оценка эффективности команды)
- 📈 **Общий балл эффективности** (0-100) - Similar to SonarQube
- 📊 **Активность команды** - Commits, PRs, active contributors
- ⏱️ **Скорость ревью** - Average time to first review
- 👥 **Коллаборация** - Team collaboration metrics
- 🚨 **Алерты** - Automated alerts when scores drop

#### 2. Technical Debt Analysis (Анализ технического долга)
- 🧪 **Test Coverage Trends** - Tracking test coverage changes
- 📝 **TODO Growth** - Monitoring TODO comments accumulation
- 💬 **Review Quality** - Code review comment density
- 📉 **Debt Score** - Overall technical debt indicator
- 💡 **Recommendations** - Actionable improvement suggestions

#### 3. Bottleneck Analysis (Анализ узких мест)
- 🔍 **Stage Identification** - Which stage is slowest (todo, dev, review, testing)
- ⏰ **Time Tracking** - Average time in each stage
- 📊 **Impact Assessment** - How severe is the bottleneck
- 🎯 **Recommendations** - Specific suggestions to improve workflow

## 📖 API Documentation

После запуска backend сервера, документация API доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Основные эндпоинты / Main Endpoints

#### Projects (T1 Сфера.Код Projects)
- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create project
- `POST /api/v1/projects/{id}/generate-mock-data` - Generate mock T1 data

#### Teams
- `GET /api/v1/teams` - List teams
- `POST /api/v1/teams` - Create team
- `POST /api/v1/teams/members` - Add team member

#### Metrics & Analysis
- `GET /api/v1/metrics/team/{id}/effectiveness` - Team effectiveness score
- `GET /api/v1/metrics/team/{id}/technical-debt` - Technical debt analysis
- `GET /api/v1/metrics/team/{id}/bottlenecks` - Bottleneck analysis
- `GET /api/v1/metrics/project/{id}/technical-debt` - Project technical debt

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