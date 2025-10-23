# Миграция на новое ТЗ: Только Git-данные

## Изменения в техническом задании

### Было (старое ТЗ)
Система интегрировалась с T1 Сфера.Код и получала данные о:
- Коммитах
- Pull Requests
- Code Reviews
- Задачах/Issues

### Стало (новое ТЗ)
Система получает данные ТОЛЬКО о:
- Git коммитах
- Ветках
- Репозиториях  
- Diff коммитов

## Доступные эндпоинты T1 Сфера.Код

| Описание                           |  Метод | URL                                                    |
|------------------------------------|-------:|--------------------------------------------------------|
| Запросить список проектов          |    GET | /projects                                              |
| Запросить информацию по проекту    |    GET | /projects/{projectKey}                                 |
| Запросить список репозиториев      |    GET | /projects/{projectKey}/repos                           |
| Запросить информации о репозитории |    GET | /projects/{projectKey}/repos/{repoName}                |
| Запросить список веток репозитория |    GET | /projects/{projectKey}/repos/{repoName}/branches       |
| Запросить список коммитов          |    GET | /projects/{projectKey}/repos/{repoName}/commits        |
| Запросить diff коммита             |    GET | /projects/{projectKey}/repos/{repoName}/commits/{sha1} |

**Важно:** "Проект" - это совокупность репозиториев. Репозитории хранят git данные.

## Изменения в метриках

### 1. Технический долг (Technical Debt)

#### Было:
- ✅ Покрытие тестами (test coverage)
- ✅ TODO в коде
- ✅ TODO в ревью
- ✅ Code churn rate
- ✅ Качество ревью (review comment density)

#### Стало:
- ✅ **TODO из diff коммитов** (ЕДИНСТВЕННАЯ метрика)
- ❌ Покрытие тестами (нет данных)
- ❌ TODO в ревью (нет PR/Review данных)
- ❌ Code churn (убрано из анализа)
- ❌ Качество ревью (нет Review данных)

**Новая логика:**
- 0 TODO = 0 баллов долга (отлично)
- До 10 TODO = низкий долг
- 10-30 TODO = умеренный долг
- 30-50 TODO = заметный долг
- 50-100 TODO = много долга
- 100+ TODO = критический долг
- 200+ TODO = 100 баллов долга

### 2. Забота о сотрудниках (Employee Care)

#### Статус: ✅ БЕЗ ИЗМЕНЕНИЙ

Анализ основан на временных метках коммитов:
- Процент коммитов после рабочего времени
- Процент коммитов в выходные дни
- Оценка заботы о сотрудниках (0-100)
- Рекомендации по улучшению work-life balance

**Данная метрика полностью работает на основе git-данных.**

### 3. Активные участники (Active Contributors)

#### Статус: ✅ НОВАЯ МЕТРИКА

Количество активных участников для оценки затрат человеческих ресурсов:
- Берутся все коммиты за период (по умолчанию 30 дней)
- Подсчитываются уникальные авторы
- Каждый уникальный автор = активный участник
- Среднее количество коммитов на участника

**Эндпоинт:** `GET /api/v1/metrics/project/{id}/active-contributors`

### 4. Количество коммитов на человека (Commits Per Person)

#### Статус: ✅ НОВАЯ МЕТРИКА

Для понимания уровня экспертности по проекту:
- Количество коммитов каждого участника
- Количество измененных строк кода
- Уровень экспертности:
  - `beginner`: < 5 коммитов
  - `intermediate`: 5-19 коммитов
  - `advanced`: 20-49 коммитов
  - `expert`: 50+ коммитов
- Сортировка по количеству коммитов (убывание)

**Эндпоинт:** `GET /api/v1/metrics/project/{id}/commits-per-person`

### 5. Эффективность проекта (Effectiveness Score)

#### Было:
- Активность коммитов (20 баллов)
- Производительность PR (20 баллов)
- Эффективность ревью (20 баллов)
- Вовлеченность команды (20 баллов)
- Work-life balance (10 баллов)
- Качество кода (10 баллов)

#### Стало:
- Активность коммитов (30 баллов)
- Вовлеченность команды (30 баллов)
- Work-life balance (20 баллов)
- Качество кода / Code churn (20 баллов)

**Изменения:**
- Убраны метрики, связанные с PR и ревью
- Увеличены веса для доступных метрик
- Максимум: 100 баллов

### 6. Анализ узких мест (Bottlenecks)

#### Статус: ⚠️ УСТАРЕЛО (DEPRECATED)

**Причина:** Требует данных о задачах (Tasks) с временем в каждой стадии:
- time_in_todo
- time_in_development
- time_in_review
- time_in_testing

**Рекомендация:** Не использовать в новом ТЗ. Эндпоинт оставлен для совместимости, но вернет пустые данные или данные на основе mock-данных.

## Изменения в API

### Новые эндпоинты

```
GET /api/v1/metrics/project/{id}/active-contributors
GET /api/v1/metrics/project/{id}/commits-per-person
```

### Обновленные эндпоинты

```
GET /api/v1/metrics/project/{id}/technical-debt
    - Теперь возвращает ТОЛЬКО данные о TODO
    - Убраны поля: test_coverage, test_coverage_trend, todo_in_reviews, churn_rate, review_comment_density

GET /api/v1/metrics/project/{id}/effectiveness
    - Убраны поля: total_prs, avg_pr_review_time
    - Обновлена логика расчета оценки
```

### Устаревшие эндпоинты

```
GET /api/v1/metrics/project/{id}/bottlenecks
    - DEPRECATED: требует Task данные

GET /api/v1/metrics/project/{id}/prs-needing-attention
    - DEPRECATED: требует PR данные
```

## Изменения в схемах данных (Schemas)

### TechnicalDebtAnalysis

**Было:**
```python
{
    "team_id": int,
    "project_id": int,
    "test_coverage": float,
    "test_coverage_trend": str,
    "todo_count": int,
    "todo_in_reviews": int,
    "todo_trend": str,
    "churn_rate": float,
    "review_comment_density": float,
    "technical_debt_score": float,
    "recommendations": [str],
    "period_start": datetime,
    "period_end": datetime
}
```

**Стало:**
```python
{
    "project_id": int,
    "todo_count": int,
    "todo_trend": str,  # up, down, stable
    "technical_debt_score": float,  # 0-100
    "recommendations": [str],
    "period_start": datetime,
    "period_end": datetime
}
```

### ProjectEffectivenessMetrics

**Убрано:**
- `total_prs: int`
- `avg_pr_review_time: float`

**Оставлено:**
- `total_commits: int`
- `active_contributors: int`
- `effectiveness_score: float`
- `after_hours_percentage: float`
- `weekend_percentage: float`
- `churn_rate: float`

### Новые схемы

#### ActiveContributorsMetrics
```python
{
    "project_id": int,
    "project_name": str,
    "active_contributors": int,
    "total_commits": int,
    "avg_commits_per_contributor": float,
    "period_start": datetime,
    "period_end": datetime
}
```

#### CommitsPerPersonMetrics
```python
{
    "project_id": int,
    "project_name": str,
    "contributors": [
        {
            "author_id": int,
            "author_name": str,
            "author_email": str,
            "commit_count": int,
            "lines_changed": int,
            "expertise_level": str  # beginner, intermediate, advanced, expert
        }
    ],
    "total_contributors": int,
    "period_start": datetime,
    "period_end": datetime
}
```

## Миграция данных

### Модели базы данных

**Статус:** БЕЗ ИЗМЕНЕНИЙ

Модели `PullRequest`, `Task`, `CodeReview` оставлены в базе данных для:
1. Обратной совместимости
2. Возможности работы с mock-данными
3. Возможного будущего расширения

Однако новые метрики их **не используют**.

### Существующие данные

Если в базе есть данные о PR/Tasks/Reviews:
- Они сохраняются
- Не используются в новых метриках
- Могут использоваться для тестирования

## Рекомендации по использованию

### Основные метрики для анализа проекта

1. **Эффективность:** `GET /metrics/project/{id}/effectiveness`
   - Получить общую оценку проекта
   - Понять активность команды

2. **Активные участники:** `GET /metrics/project/{id}/active-contributors`
   - Оценить затраты человеческих ресурсов
   - Понять размер активной команды

3. **Экспертность:** `GET /metrics/project/{id}/commits-per-person`
   - Определить ключевых участников
   - Оценить распределение знаний

4. **Забота о сотрудниках:** `GET /metrics/project/{id}/employee-care`
   - Выявить переработки
   - Предотвратить выгорание команды

5. **Технический долг:** `GET /metrics/project/{id}/technical-debt`
   - Отследить накопление TODO
   - Спланировать работу по устранению долга

## Обновление фронтенда

### Компоненты для обновления

1. **Dashboard страница**
   - Обновить виджеты метрик
   - Убрать PR-based метрики
   - Добавить новые метрики (Active Contributors, Commits Per Person)

2. **Metrics страница**
   - Обновить графики эффективности
   - Добавить визуализацию экспертности
   - Обновить отображение технического долга

3. **API клиент (composables/useApi.ts)**
   - Обновить типы для схем
   - Добавить методы для новых эндпоинтов

## Тестирование

Все существующие тесты обновлены:
- ✅ 12/12 тестов проходят успешно
- ✅ Добавлены тесты для новых метрик
- ✅ Обновлены тесты для измененных метрик

## Совместимость

### Обратная совместимость

**Частичная:**
- Старые эндпоинты оставлены
- Устаревшие эндпоинты помечены как DEPRECATED
- Схемы данных изменены (breaking change для клиентов)

### Рекомендации по миграции клиентов

1. Обновить схемы данных в клиентском коде
2. Заменить вызовы к устаревшим эндпоинтам
3. Добавить обработку новых метрик
4. Протестировать интеграцию

## Заключение

Система успешно адаптирована под новое ТЗ с ограничением на git-данные. Все ключевые метрики доступны и основаны исключительно на информации из коммитов, веток и diff'ов.

**Ключевые преимущества:**
- ✅ Проще интеграция (меньше эндпоинтов для подключения)
- ✅ Быстрее сбор данных (только git операции)
- ✅ Независимость от PR/Issue tracking систем
- ✅ Фокус на реальной активности разработчиков

**Ограничения:**
- ❌ Нет метрик скорости ревью
- ❌ Нет анализа узких мест в workflow
- ❌ Нет метрик покрытия тестами
- ❌ Ограниченный анализ технического долга (только TODO)
