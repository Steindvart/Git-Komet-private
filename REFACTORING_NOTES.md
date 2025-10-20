# Рефакторинг под требования хакатона / Refactoring for Hackathon Requirements

## Изменения / Changes

Система была переработана в соответствии с актуальными требованиями хакатона: интеграция с **Т1 Сфера.Код** и анализ метрик команд.

The system has been refactored according to the actual hackathon requirements: integration with **T1 Сфера.Код** and team metrics analysis.

## Основные изменения / Main Changes

### 1. Изменение модели данных / Data Model Changes

**Было / Before:**
- Repository (Git репозитории)
- Commits (коммиты из Git)
- Простые метрики

**Стало / After:**
- **Project** (проекты из T1 Сфера.Код)
- **Commit** (с данными о покрытии тестами и TODO)
- **PullRequest** (с временем ревью)
- **CodeReview** (с количеством комментариев)
- **Task** (с временем на каждом этапе)
- **TeamMetric** (с алертами и трендами)
- **TechnicalDebtMetric** (отслеживание технического долга)

### 2. Три направления анализа / Three Analysis Directions

#### A. Team Effectiveness Score (Оценка эффективности команды)
- **Балл 0-100** - как в SonarQube
- Учитывает:
  - Активность коммитов
  - Пропускную способность PR
  - Эффективность ревью
  - Коллаборацию команды
- **Алерты** при снижении показателей
- **Тренды** (improving, stable, declining)

**API:** `GET /api/v1/metrics/team/{id}/effectiveness`

#### B. Technical Debt Analysis (Анализ технического долга)
- **Test Coverage Trends** - отслеживание покрытия тестами
  - Тренд (up/down/stable)
  - Изменение покрытия
- **TODO Growth** - рост количества TODO
  - Количество и тренд
- **Review Comment Density** - плотность комментариев в ревью
  - Комментариев на PR
- **Debt Score** - общий балл технического долга
- **Рекомендации** по улучшению

**API:** `GET /api/v1/metrics/team/{id}/technical-debt`

#### C. Bottleneck Analysis (Анализ узких мест)
- **Определение узкого места** - какой этап самый медленный:
  - TODO (задача висит в бэклоге)
  - Development (разработка)
  - Review (code review)
  - Testing (тестирование)
- **Среднее время** на каждом этапе
- **Impact Score** - насколько серьезно узкое место
- **Рекомендации** по улучшению workflow

**API:** `GET /api/v1/metrics/team/{id}/bottlenecks`

### 3. Mock данные из T1 API / Mock Data from T1 API

Добавлен сервис для генерации mock-данных, имитирующих данные из T1 Сфера.Код:

**API:** `POST /api/v1/projects/{id}/generate-mock-data?team_id=1`

Генерирует:
- **Commits** (50) с:
  - Покрытием тестами (has_tests, test_coverage_delta)
  - Количеством TODO (todo_count)
- **Pull Requests** (20) с:
  - Временем до первого ревью (time_to_first_review)
  - Временем до merge (time_to_merge)
  - Количеством циклов ревью (review_cycles)
- **Code Reviews** с:
  - Количеством комментариев
  - Критическими комментариями
- **Tasks** (30) с:
  - Временем в каждом статусе (time_in_todo, time_in_development, time_in_review, time_in_testing)

### 4. Обновленный Frontend / Updated Frontend

#### Dashboard
- Обзор трех направлений анализа
- Quick start guide
- Статистика

#### Projects (было Repositories)
- Управление проектами из T1
- Генерация mock-данных
- Удален функционал клонирования Git

#### Analytics (было Metrics)
- **Team Effectiveness Score** с визуализацией:
  - Круговой индикатор балла
  - Алерты (warning/critical)
  - Тренды
- **Technical Debt** с метриками:
  - Test coverage с прогресс-баром
  - TODO count с трендом
  - Review comment density
  - Debt score
  - Рекомендации
- **Bottlenecks** с визуализацией:
  - Определение узкого места
  - Impact score
  - Breakdown по этапам
  - Рекомендации

### 5. Удалены ненужные зависимости / Removed Unnecessary Dependencies

- ❌ **GitPython** - не нужен, т.к. работаем с T1 API
- ❌ Git клонирование - не нужно
- ❌ Repository sync - заменено на mock data generation

## Как использовать / How to Use

### 1. Создать проект / Create Project
```bash
POST /api/v1/projects
{
  "name": "My Project",
  "external_id": "t1_project_123",
  "description": "Project from T1"
}
```

### 2. Создать команду / Create Team
```bash
POST /api/v1/teams
{
  "name": "Development Team",
  "description": "Main dev team"
}

POST /api/v1/teams/members
{
  "team_id": 1,
  "email": "dev@example.com",
  "name": "Developer Name"
}
```

### 3. Сгенерировать mock-данные / Generate Mock Data
```bash
POST /api/v1/projects/1/generate-mock-data?team_id=1
```

Это создаст:
- 50 коммитов
- 20 pull requests
- ~40 code reviews
- 30 задач

### 4. Получить аналитику / Get Analytics

**Team Effectiveness:**
```bash
GET /api/v1/metrics/team/1/effectiveness?period_days=30
```

**Technical Debt:**
```bash
GET /api/v1/metrics/team/1/technical-debt?period_days=30
```

**Bottlenecks:**
```bash
GET /api/v1/metrics/team/1/bottlenecks?period_days=30
```

## Преимущества подхода / Approach Benefits

1. ✅ **Соответствие требованиям хакатона** - интеграция с T1 Сфера.Код
2. ✅ **Три направления анализа** - effectiveness, technical debt, bottlenecks
3. ✅ **SonarQube-style scoring** - понятная оценка 0-100
4. ✅ **Алерты и рекомендации** - actionable insights
5. ✅ **Mock данные** - можно демонстрировать без реального T1 API
6. ✅ **Упрощение** - не нужно работать с Git напрямую
7. ✅ **Расширяемость** - легко добавить новые метрики

## Следующие шаги / Next Steps

1. ✅ Базовая структура реализована
2. 🔄 Можно добавить:
   - Визуализацию трендов (графики Chart.js)
   - Исторические данные
   - Сравнение команд
   - Export отчетов
   - Настройка целевых значений (targets)
3. 🔄 Интеграция с реальным T1 API (когда появится доступ)

## Commit Hash

Изменения зафиксированы в коммите: `f542a5c`
