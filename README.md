# Git-Komet

Система автооценки эффективности команд через анализ Git-метрик.
Team Effectiveness Analysis System Through Git Metrics from T1 Сфера.Код.

## 📋 Описание / Description

Git-Komet - это система для анализа эффективности работы команд разработки через метрики из T1 Сфера.Код. Проект разработан для участия в хакатоне на тему "Разработайте систему автооценки эффективности команд через анализ Git-метрик".

Git-Komet is a system for analyzing development team effectiveness through metrics from T1 Сфера.Код (Sphere.Code). The project is developed for a hackathon on the theme "Develop a system for automatic team effectiveness evaluation through Git metrics analysis".

### Интеграция с T1 Сфера.Код / T1 Sphere.Code Integration

Система интегрируется с T1 Сфера.Код и собирает данные о:
- Коммитах (commits)
- Ветках (branches)
- Репозиториях (repositories)
- Diff коммитов (commit diffs)

The system integrates with T1 Sphere.Code and collects data about:
- Commits
- Branches
- Repositories
- Commit diffs

**Доступные эндпоинты / Available Endpoints:**

| Описание                           |  Метод | URL                                                    |
|------------------------------------|-------:|--------------------------------------------------------|
| Запросить список проектов          |    GET | /projects                                              |
| Запросить информацию по проекту    |    GET | /projects/{projectKey}                                 |
| Запросить список репозиториев      |    GET | /projects/{projectKey}/repos                           |
| Запросить информации о репозитории |    GET | /projects/{projectKey}/repos/{repoName}                |
| Запросить список веток репозитория |    GET | /projects/{projectKey}/repos/{repoName}/branches       |
| Запросить список коммитов          |    GET | /projects/{projectKey}/repos/{repoName}/commits        |
| Запросить diff коммита             |    GET | /projects/{projectKey}/repos/{repoName}/commits/{sha1} |

**Важно:** "Проект" - это совокупность репозиториев. Репозитории в свою очередь хранят в себе информацию с git данными.

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

- ✅ **Интеграция с T1 Сфера.Код** - Получение данных из git-репозиториев (коммиты, ветки, diff)
- ✅ **Управление проектами** - Создание проектов и добавление участников
- ✅ **Анализ эффективности проектов** - Комплексная оценка производительности (0-100)
- ✅ **Анализ технического долга** - Отслеживание TODO комментариев из diff коммитов
- ✅ **Анализ переработок** - Забота о сотрудниках (работа после часов и в выходные)
- ✅ **Анализ активных участников** - Количество уникальных авторов коммитов
- ✅ **Анализ экспертности** - Количество коммитов на человека для оценки уровня знаний
- ✅ **Визуализация данных** - Графики и дашборды для отображения метрик
- ✅ **Алерты и рекомендации** - Автоматические уведомления о проблемах
- ✅ **Тренды** - Отслеживание изменений метрик во времени
- ✅ **RESTful API** - Полноценный API для интеграции

### Анализируемые метрики / Analyzed Metrics

#### 1. Project Effectiveness Score (Оценка эффективности проекта)
- 📈 **Общий балл эффективности** (0-100) - Based on commit activity and work-life balance
- 📊 **Активность команды** - Total commits, active contributors
- 👥 **Вовлеченность** - Team collaboration through commit patterns
- 🚨 **Алерты** - Automated alerts when scores drop or issues detected

#### 2. Technical Debt Analysis (Анализ технического долга)
- 📝 **TODO из diff** - Мониторинг TODO комментариев из коммитов
- 📈 **TODO тренды** - Отслеживание роста/снижения TODO
- 📉 **Debt Score** - Оценка технического долга на основе TODO (0-100, меньше лучше)
- 💡 **Рекомендации** - Конкретные предложения по устранению долга

#### 3. Employee Care Analysis (Забота о сотрудниках)
- ⏰ **Переработки** - Процент коммитов после рабочего времени
- 📅 **Работа в выходные** - Процент коммитов в выходные дни
- 💚 **Care Score** - Оценка заботы о сотрудниках (0-100, больше лучше)
- 📊 **Статус** - Excellent, Good, Needs Attention, Critical
- 💡 **Рекомендации** - Советы по улучшению work-life balance

#### 4. Active Contributors Analysis (Анализ активных участников)
- 👥 **Активные участники** - Количество уникальных авторов коммитов за период
- 📊 **Общее количество коммитов** - Активность проекта
- 📈 **Среднее на участника** - Commits per contributor
- 🎯 **Ресурсы проекта** - Понимание затрат человеческих ресурсов

#### 5. Expertise Level Analysis (Анализ экспертности)
- 🏆 **Коммиты на человека** - Детальная статистика по каждому участнику
- 📊 **Измененные строки** - Lines of code contributed
- 🎓 **Уровень экспертности** - Beginner, Intermediate, Advanced, Expert
- 📈 **Рейтинг участников** - Сортировка по вкладу в проект

## 📖 API Documentation

После запуска backend сервера, документация API доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Основные эндпоинты / Main Endpoints

#### Projects (Git Repositories)
- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create project
- `POST /api/v1/projects/{id}/generate-mock-data` - Generate mock data

#### Project Members
- `GET /api/v1/teams` - List project members (legacy endpoint name)
- `POST /api/v1/teams` - Create project
- `POST /api/v1/teams/members` - Add project member

#### Metrics & Analysis

##### Эффективность проекта / Project Effectiveness
- `GET /api/v1/metrics/project/{id}/effectiveness` - Project effectiveness score
- `GET /api/v1/metrics/project/{id}/active-contributors` - **NEW:** Active contributors analysis
- `GET /api/v1/metrics/project/{id}/commits-per-person` - **NEW:** Commits per person (expertise level)

##### Забота о сотрудниках / Employee Care  
- `GET /api/v1/metrics/project/{id}/employee-care` - Employee care metrics (overwork analysis)

##### Технический долг / Technical Debt
- `GET /api/v1/metrics/project/{id}/technical-debt` - Technical debt analysis (TODO comments only)

##### Узкие места / Bottlenecks (DEPRECATED - requires PR/Task data)
- `GET /api/v1/metrics/project/{id}/bottlenecks` - Bottleneck analysis
- `GET /api/v1/metrics/project/{id}/prs-needing-attention` - PRs needing attention

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