# Архитектура Git-Komet / Architecture

## Обзор системы / System Overview

Git-Komet - это система для автоматической оценки эффективности команд разработки через анализ Git-метрик. Система состоит из backend API и frontend веб-приложения.

## Архитектурная диаграмма / Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (Nuxt.js)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │Dashboard │  │Repos Page│  │Teams Page│  │Metrics  │ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬────┘ │
│       │             │              │             │       │
│       └─────────────┴──────────────┴─────────────┘       │
│                     │                                     │
│              ┌──────▼──────┐                             │
│              │  useApi()   │  (Composable)               │
│              └──────┬──────┘                             │
└─────────────────────┼────────────────────────────────────┘
                      │ HTTP/REST API
                      │
┌─────────────────────▼────────────────────────────────────┐
│                Backend (FastAPI)                          │
│  ┌──────────────────────────────────────────────────┐   │
│  │              API Layer                            │   │
│  │  ┌────────┐  ┌────────┐  ┌────────┐             │   │
│  │  │Repos   │  │Teams   │  │Metrics │             │   │
│  │  │Endpoint│  │Endpoint│  │Endpoint│             │   │
│  │  └───┬────┘  └───┬────┘  └───┬────┘             │   │
│  └──────┼───────────┼───────────┼──────────────────┘   │
│         │           │           │                       │
│  ┌──────▼───────────▼───────────▼──────────────────┐   │
│  │           Services Layer                         │   │
│  │  ┌──────────────┐    ┌─────────────────┐       │   │
│  │  │  GitService  │    │ MetricsService  │       │   │
│  │  │              │    │                 │       │   │
│  │  │ - clone      │    │ - calculate     │       │   │
│  │  │ - extract    │    │ - analyze       │       │   │
│  │  │ - analyze    │    │ - aggregate     │       │   │
│  │  └──────┬───────┘    └────────┬────────┘       │   │
│  └─────────┼─────────────────────┼────────────────┘   │
│            │                     │                     │
│  ┌─────────▼─────────────────────▼────────────────┐   │
│  │              ORM Layer (SQLAlchemy)             │   │
│  │  ┌──────────┐ ┌──────┐ ┌──────┐ ┌──────────┐  │   │
│  │  │Repository│ │Team  │ │Commit│ │Metric    │  │   │
│  │  │Model     │ │Model │ │Model │ │Model     │  │   │
│  │  └──────────┘ └──────┘ └──────┘ └──────────┘  │   │
│  └─────────────────────┬─────────────────────────┘   │
└────────────────────────┼─────────────────────────────┘
                         │
                    ┌────▼────┐
                    │ SQLite  │
                    │Database │
                    └─────────┘
```

## Компоненты системы / System Components

### Frontend (Nuxt.js + Vue.js)

#### Структура страниц / Page Structure

1. **Dashboard (`/`)**
   - Обзор системы
   - Статистика
   - Быстрые действия

2. **Repositories (`/repositories`)**
   - Список репозиториев
   - Добавление нового репозитория
   - Синхронизация коммитов
   - Управление репозиториями

3. **Teams (`/teams`)**
   - Список команд
   - Создание команды
   - Добавление участников
   - Управление командами

4. **Metrics (`/metrics`)**
   - Визуализация метрик
   - Графики эффективности
   - Аналитика по командам
   - Аналитика по репозиториям

#### Ключевые компоненты / Key Components

- **Chart.vue** - Компонент для визуализации данных
- **useApi composable** - HTTP клиент для API
- **layouts/default.vue** - Основной layout с навигацией

### Backend (FastAPI + Python)

#### API Endpoints

##### Repositories API (`/api/v1/repositories`)
- `GET /` - Список репозиториев
- `POST /` - Создать репозиторий
- `GET /{id}` - Получить репозиторий
- `PUT /{id}` - Обновить репозиторий
- `DELETE /{id}` - Удалить репозиторий
- `POST /{id}/sync` - Синхронизировать коммиты

##### Teams API (`/api/v1/teams`)
- `GET /` - Список команд
- `POST /` - Создать команду
- `GET /{id}` - Получить команду
- `DELETE /{id}` - Удалить команду
- `POST /members` - Добавить участника
- `GET /{id}/members` - Список участников
- `DELETE /members/{id}` - Удалить участника

##### Metrics API (`/api/v1/metrics`)
- `GET /team/{id}/effectiveness` - Метрики эффективности команды
- `GET /repository/{id}` - Метрики репозитория
- `POST /repository/{id}/calculate` - Рассчитать и сохранить метрики

#### Services Layer

##### GitService
Отвечает за работу с Git-репозиториями:
- Клонирование репозиториев
- Извлечение информации о коммитах
- Анализ изменений кода
- Сбор статистики

##### MetricsService
Отвечает за расчет метрик:
- Частота коммитов
- Code churn (изменения кода)
- Активные участники
- Размер коммитов
- Эффективность команды

#### Data Models

##### Repository
```python
- id: int
- name: str
- url: str
- description: str
- created_at: datetime
- updated_at: datetime
```

##### Team
```python
- id: int
- name: str
- description: str
- created_at: datetime
```

##### TeamMember
```python
- id: int
- team_id: int
- email: str
- name: str
- role: str
- joined_at: datetime
```

##### Commit
```python
- id: int
- repository_id: int
- author_id: int
- sha: str
- message: str
- author_email: str
- author_name: str
- committed_at: datetime
- files_changed: int
- insertions: int
- deletions: int
```

##### Metric
```python
- id: int
- repository_id: int
- metric_type: str
- metric_value: str (JSON)
- period_start: datetime
- period_end: datetime
- calculated_at: datetime
```

## Поток данных / Data Flow

### 1. Добавление репозитория / Adding a Repository

```
User → Frontend → POST /api/v1/repositories
                     ↓
              Backend API validates data
                     ↓
              Create Repository in DB
                     ↓
              Return Repository object → Frontend → Display
```

### 2. Синхронизация коммитов / Syncing Commits

```
User → Frontend → POST /api/v1/repositories/{id}/sync
                     ↓
              Backend API
                     ↓
              GitService.clone_or_open_repository()
                     ↓
              GitService.extract_commits()
                     ↓
              GitService.save_commits_to_db()
                     ↓
              Return sync result → Frontend → Display
```

### 3. Расчет метрик / Calculating Metrics

```
User → Frontend → GET /api/v1/metrics/team/{id}/effectiveness
                     ↓
              Backend API
                     ↓
              MetricsService.calculate_team_effectiveness()
                     ↓
              Query commits from DB
                     ↓
              Calculate metrics:
                - Total commits
                - Lines changed
                - Commit frequency
                - Average commit size
                - Active contributors
                     ↓
              Return metrics → Frontend → Visualize
```

## Технологический стек / Technology Stack

### Backend
- **FastAPI** - Веб-фреймворк
- **SQLAlchemy** - ORM
- **SQLite** - База данных
- **GitPython** - Работа с Git
- **Pydantic** - Валидация данных
- **Uvicorn** - ASGI сервер

### Frontend
- **Nuxt.js 3** - Фреймворк
- **Vue.js 3** - UI библиотека
- **TypeScript** - Типизация
- **Chart.js** - Визуализация
- **Nuxt UI** - UI компоненты

## Метрики и аналитика / Metrics and Analytics

### Доступные данные / Available Data

В новом ТЗ доступны только git коммиты, ветки, репозитории и diff коммитов.
Все метрики рассчитываются на основе этих данных.

### Метрики проекта / Project Metrics

1. **Effectiveness Score (Оценка эффективности)**
   - Общая оценка эффективности проекта (0-100)
   - Основана на активности коммитов и вовлеченности команды
   - Учитывает work-life balance
   - Показывает качество работы (code churn rate)

2. **Active Contributors (Активные участники)**
   - Уникальные авторы коммитов за период
   - Показывает затраты человеческих ресурсов на проект
   - Среднее количество коммитов на участника

3. **Commits Per Person (Коммиты на человека)**
   - Количество коммитов каждого участника
   - Уровень экспертности (beginner, intermediate, advanced, expert)
   - Количество измененных строк кода
   - Ранжирование участников по вкладу

4. **Employee Care (Забота о сотрудниках)**
   - Процент коммитов после рабочего времени
   - Процент коммитов в выходные дни
   - Общая оценка заботы о сотрудниках (0-100)
   - Статус: excellent, good, needs_attention, critical

5. **Technical Debt (Технический долг)**
   - Количество TODO комментариев из diff коммитов
   - Тренд TODO (растет/снижается/стабильно)
   - Оценка технического долга (0-100, меньше лучше)
   - Рекомендации по устранению долга

### Устаревшие метрики / Deprecated Metrics

Следующие метрики требуют данных о PR/MR и задачах, которые недоступны в новом ТЗ:
- Review time metrics (требует PR data)
- Bottleneck analysis (требует Task data)
- Test coverage tracking (требует CI/CD integration)
- Review quality metrics (требует CodeReview data)

## Безопасность / Security

### Backend Security
- CORS настройки для разрешенных origins
- Валидация входных данных через Pydantic
- SQL injection protection через SQLAlchemy ORM

### Frontend Security
- XSS protection через Vue.js
- CSRF protection
- Secure API calls

## Масштабирование / Scalability

### Горизонтальное масштабирование / Horizontal Scaling
- Backend: Несколько инстансов за load balancer
- Database: Переход на PostgreSQL/MySQL для production
- Cache: Добавление Redis для кэширования

### Вертикальное масштабирование / Vertical Scaling
- Увеличение ресурсов сервера
- Оптимизация запросов к БД
- Индексирование таблиц

## Мониторинг и логирование / Monitoring and Logging

Рекомендуется добавить:
- Логирование запросов API
- Метрики производительности
- Error tracking (Sentry)
- APM (Application Performance Monitoring)

## Развертывание / Deployment

### Development
- Docker Compose для локальной разработки
- Hot reload для быстрой итерации

### Production
- Kubernetes для оркестрации контейнеров
- CI/CD pipeline (GitHub Actions, GitLab CI)
- Мониторинг и алертинг
- Автоматическое масштабирование
