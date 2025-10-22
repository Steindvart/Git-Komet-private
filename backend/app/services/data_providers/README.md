# Поставщики данных для Git-Komet

Этот пакет содержит поставщики данных, которые получают метрики Git из различных источников. Архитектура разработана для легкого расширения, позволяя переключаться между mock-данными и реальными источниками данных с минимальными изменениями кода.

## Обзор архитектуры

Архитектура поставщиков данных использует **паттерн Стратегия**:

```
BaseDataProvider (Абстрактный интерфейс)
    ├── MockDataProvider (Текущая реализация)
    ├── T1DataProvider (Будет реализовано)
    ├── GitHubDataProvider (Будет реализовано)
    └── GitLabDataProvider (Будет реализовано)
```

## Доступные поставщики

### MockDataProvider (По умолчанию)

Генерирует реалистичные mock-данные для целей демонстрации. Это текущий поставщик по умолчанию, который симулирует данные из системы Git-репозитория.

**Сценарий использования:** Разработка, тестирование, демо, когда реальные источники данных недоступны.

### T1DataProvider (Запланировано)

Будет интегрироваться с T1 Сфера.Код API для получения реальных метрик Git.

**Статус:** Будет реализовано при доступности T1 API.

### GitHubDataProvider (Запланировано)

Будет интегрироваться с GitHub API для получения метрик репозитория.

**Статус:** Запланировано для будущей реализации.

### GitLabDataProvider (Запланировано)

Будет интегрироваться с GitLab API для получения метрик репозитория.

**Статус:** Запланировано для будущей реализации.

## Использование

### Использование поставщика по умолчанию

```python
from app.services.data_providers import DataProviderFactory

# Создать экземпляр поставщика (по умолчанию используется 'mock')
provider = DataProviderFactory.create()

# Заполнить данные
result = provider.populate_data(db, team_id=1, project_id=1)
```

### Переключение поставщиков

```python
# Вариант 1: Установить поставщика по умолчанию глобально
DataProviderFactory.set_default('t1')  # После реализации

# Вариант 2: Запросить конкретного поставщика
provider = DataProviderFactory.create('github')  # После реализации
```

### Доступные методы поставщика

Все поставщики реализуют следующие методы:

- `fetch_commits(db, team_id, project_id, period_start, period_end)` - Получить данные коммитов
- `fetch_pull_requests(db, team_id, project_id, period_start, period_end)` - Получить данные PR
- `fetch_code_reviews(db, pull_request_ids, team_id)` - Получить данные ревью
- `fetch_tasks(db, team_id, project_id, period_start, period_end)` - Получить данные задач/issues
- `populate_data(db, team_id, project_id, period_start, period_end)` - Высокоуровневый метод для получения и сохранения всех данных

## Реализация нового поставщика

Для добавления нового поставщика данных (например, для T1 Сфера.Код):

### 1. Создать класс поставщика

Создайте новый файл `t1_provider.py` в этом каталоге:

```python
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from .base_provider import BaseDataProvider

class T1DataProvider(BaseDataProvider):
    """Поставщик данных для T1 Сфера.Код API."""
    
    def __init__(self, api_key: str, api_url: str):
        """Инициализация с учетными данными T1 API."""
        self.api_key = api_key
        self.api_url = api_url
        # Инициализировать клиент T1 API
        # self.client = T1ApiClient(api_key, api_url)
    
    def fetch_commits(self, db, team_id, project_id, period_start, period_end) -> List[Dict]:
        """Получить реальные коммиты из T1 API."""
        # Вызвать T1 API
        # commits = self.client.get_commits(project_id, period_start, period_end)
        
        # Преобразовать ответ T1 в наш формат
        # return [self._transform_commit(c) for c in commits]
        pass
    
    def fetch_pull_requests(self, db, team_id, project_id, period_start, period_end) -> List[Dict]:
        """Получить реальные PR из T1 API."""
        pass
    
    def fetch_code_reviews(self, db, pull_request_ids, team_id) -> List[Dict]:
        """Получить реальные ревью из T1 API."""
        pass
    
    def fetch_tasks(self, db, team_id, project_id, period_start, period_end) -> List[Dict]:
        """Получить реальные задачи из T1 API."""
        pass
    
    def populate_data(self, db, team_id, project_id, period_start=None, period_end=None) -> Dict:
        """Заполнить базу данных реальными данными из T1."""
        # Реализовать аналогично MockDataProvider.populate_data()
        # но используя реальные вызовы API вместо генерации mock-данных
        pass
```

### 2. Зарегистрировать поставщика

Обновите `__init__.py`:

```python
from .t1_provider import T1DataProvider

__all__ = [..., 'T1DataProvider']
```

Обновите `provider_factory.py`:

```python
from .t1_provider import T1DataProvider

class DataProviderFactory:
    _providers = {
        'mock': MockDataProvider,
        't1': T1DataProvider,  # Добавить здесь
        # ...
    }
```

### 3. Настройка и использование

```python
# В вашей конфигурации или окружении
from app.services.data_providers import DataProviderFactory, T1DataProvider

# Зарегистрировать с конфигурацией
DataProviderFactory.register_provider('t1', T1DataProvider)

# Установить по умолчанию
DataProviderFactory.set_default('t1')

# Или использовать напрямую
provider = DataProviderFactory.create('t1')
result = provider.populate_data(db, team_id=1, project_id=1)
```

## Требования к формату данных

Все поставщики должны возвращать данные в следующих форматах (см. `base_provider.py` для подробной документации):

### Коммиты
```python
{
    'external_id': str,          # SHA коммита
    'author_email': str,
    'author_name': str,
    'message': str,
    'committed_at': datetime,
    'files_changed': int,
    'insertions': int,
    'deletions': int,
    'has_tests': bool,
    'test_coverage_delta': float,
    'todo_count': int,
    'is_churn': bool,
    'churn_days': int,
    'is_after_hours': bool,
    'is_weekend': bool
}
```

### Pull Requests
```python
{
    'external_id': str,
    'project_id': int,
    'author_email': str,
    'title': str,
    'description': str,
    'state': str,               # open, merged, closed
    'created_at': datetime,
    'updated_at': datetime,
    'merged_at': datetime,
    'time_to_first_review': float,  # часы
    'time_to_merge': float,     # часы
    'review_cycles': int,
    'lines_added': int,
    'lines_deleted': int,
    'files_changed': int
}
```

### Code Reviews
```python
{
    'pull_request_id': int,
    'reviewer_email': str,
    'state': str,               # approved, changes_requested, commented
    'created_at': datetime,
    'comments_count': int,
    'critical_comments': int,
    'todo_comments': int
}
```

### Задачи
```python
{
    'external_id': str,
    'project_id': int,
    'assignee_email': str,
    'title': str,
    'description': str,
    'state': str,               # todo, in_progress, in_review, done
    'priority': str,            # low, medium, high, critical
    'created_at': datetime,
    'started_at': datetime,
    'completed_at': datetime,
    'time_in_todo': float,      # часы
    'time_in_development': float,  # часы
    'time_in_review': float,    # часы
    'time_in_testing': float    # часы
}
```

## Конфигурация

Вы можете настроить поставщика по умолчанию через переменные окружения:

```bash
# Файл .env
DATA_PROVIDER=mock  # Варианты: mock, t1, github, gitlab
T1_API_KEY=ваш_api_ключ
T1_API_URL=https://api.t1-sphere.com
```

Затем в вашей конфигурации:

```python
# app/core/config.py
class Settings(BaseSettings):
    DATA_PROVIDER: str = "mock"
    T1_API_KEY: Optional[str] = None
    T1_API_URL: Optional[str] = None
```

## Тестирование

Каждый поставщик должен включать тесты:

```python
# tests/test_data_providers.py
def test_mock_provider():
    provider = DataProviderFactory.create('mock')
    assert isinstance(provider, MockDataProvider)
    
def test_t1_provider():
    provider = DataProviderFactory.create('t1')
    assert isinstance(provider, T1DataProvider)
```

## Преимущества этой архитектуры

1. **Легко переключать поставщиков**: Изменить одну строку кода или конфигурацию
2. **Тестируемость**: Mock-поставщик для тестирования, реальный поставщик для продакшена
3. **Расширяемость**: Добавлять новых поставщиков без изменения существующего кода
4. **Типобезопасность**: Все поставщики реализуют один интерфейс
5. **Поддерживаемость**: Четкое разделение ответственности

## Путь миграции

Текущее: `MockDataProvider` → Будущее: `T1DataProvider` или любой другой поставщик

Миграция бесшовная - просто реализуйте нового поставщика следуя интерфейсу, зарегистрируйте его и переключите конфигурацию. Никаких изменений не требуется в коде потребителя.
