# Contributing to Git-Komet

Спасибо за интерес к проекту Git-Komet! Мы рады любому вкладу в развитие системы.

Thank you for your interest in contributing to Git-Komet! We welcome contributions from everyone.

## Как внести вклад / How to Contribute

### Сообщения об ошибках / Bug Reports

Если вы нашли ошибку:
1. Проверьте, не создан ли уже Issue для этой проблемы
2. Создайте новый Issue с подробным описанием:
   - Шаги для воспроизведения
   - Ожидаемое поведение
   - Фактическое поведение
   - Версия ОС и браузера
   - Скриншоты (если применимо)

### Предложения новых функций / Feature Requests

Есть идея для новой функции?
1. Создайте Issue с тегом "enhancement"
2. Опишите функцию и почему она будет полезна
3. Приведите примеры использования

### Pull Requests

1. **Fork репозиторий**

2. **Создайте ветку для вашей функции**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Следуйте стилю кода**
   - Backend (Python):
     - Используйте PEP 8
     - Добавьте docstrings для функций
     - Используйте type hints
   
   - Frontend (TypeScript/Vue):
     - Используйте ESLint
     - Следуйте Vue.js Style Guide
     - Используйте TypeScript типы

4. **Добавьте тесты**
   - Backend: pytest тесты в `backend/tests/`
   - Frontend: тесты компонентов

5. **Убедитесь, что тесты проходят**
   ```bash
   # Backend
   cd backend
   pytest
   
   # Frontend
   cd frontend
   npm run test
   ```

6. **Commit изменений**
   ```bash
   git commit -m "Add: описание изменений"
   ```
   
   Формат commit сообщений:
   - `Add: новая функция`
   - `Fix: исправление бага`
   - `Update: обновление существующей функции`
   - `Refactor: рефакторинг кода`
   - `Docs: изменения в документации`

7. **Push в ваш fork**
   ```bash
   git push origin feature/amazing-feature
   ```

8. **Создайте Pull Request**
   - Опишите изменения
   - Ссылайтесь на связанные Issues
   - Добавьте скриншоты для UI изменений

## Структура кода / Code Structure

### Backend (Python/FastAPI)

```
backend/
├── app/
│   ├── api/endpoints/  # API маршруты
│   ├── core/          # Конфигурация
│   ├── db/            # База данных
│   ├── models/        # SQLAlchemy модели
│   ├── schemas/       # Pydantic схемы
│   └── services/      # Бизнес-логика
└── tests/             # Тесты
```

### Frontend (Vue.js/Nuxt.js)

```
frontend/
├── assets/        # Статические ресурсы
├── components/    # Vue компоненты
├── composables/   # Composable функции
├── layouts/       # Layouts
├── pages/         # Страницы (роутинг)
└── plugins/       # Плагины
```

## Стиль кода / Code Style

### Python (Backend)

```python
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    """User model representing a team member."""
    
    id: int
    name: str
    email: str
    role: Optional[str] = None
    
    def get_full_name(self) -> str:
        """Return user's full name."""
        return self.name
```

### TypeScript/Vue (Frontend)

```typescript
// Composable
export const useApi = () => {
  const fetchData = async (): Promise<Data[]> => {
    try {
      const response = await fetch('/api/data')
      return await response.json()
    } catch (error) {
      console.error('Error fetching data:', error)
      throw error
    }
  }
  
  return { fetchData }
}
```

## Тестирование / Testing

### Backend Tests (pytest)

```python
def test_create_repository(client):
    """Test creating a repository."""
    repo_data = {
        "name": "Test Repo",
        "url": "https://github.com/test/repo.git"
    }
    response = client.post("/api/v1/repositories", json=repo_data)
    assert response.status_code == 200
    assert response.json()["name"] == repo_data["name"]
```

### Frontend Tests

```typescript
describe('Component', () => {
  it('renders correctly', () => {
    // Test implementation
  })
})
```

## Документация / Documentation

При добавлении новых функций:
1. Обновите README.md
2. Добавьте комментарии в код
3. Обновите API документацию
4. Добавьте примеры использования

## Вопросы? / Questions?

Если у вас есть вопросы:
1. Проверьте документацию
2. Посмотрите существующие Issues
3. Создайте новый Issue с тегом "question"

## Кодекс поведения / Code of Conduct

- Будьте уважительны
- Принимайте конструктивную критику
- Фокусируйтесь на том, что лучше для проекта
- Помогайте другим участникам

Спасибо за ваш вклад! 🚀

Thank you for your contributions! 🚀
