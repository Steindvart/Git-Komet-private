# Data Providers for Git-Komet

This package contains data providers that fetch Git metrics from various sources. The architecture is designed to be easily extensible, allowing you to switch between mock data and real data sources with minimal code changes.

## Architecture Overview

The data provider architecture uses the **Strategy Pattern**:

```
BaseDataProvider (Abstract Interface)
    ├── MockDataProvider (Current Implementation)
    ├── T1DataProvider (To be implemented)
    ├── GitHubDataProvider (To be implemented)
    └── GitLabDataProvider (To be implemented)
```

## Available Providers

### MockDataProvider (Default)

Generates realistic mock data for demonstration purposes. This is the current default provider and simulates data from a Git repository system.

**Use case:** Development, testing, demos, when real data sources are not available.

### T1DataProvider (Planned)

Will integrate with T1 Сфера.Код API to fetch real Git metrics.

**Status:** To be implemented when T1 API is available.

### GitHubDataProvider (Planned)

Will integrate with GitHub API to fetch repository metrics.

**Status:** Planned for future implementation.

### GitLabDataProvider (Planned)

Will integrate with GitLab API to fetch repository metrics.

**Status:** Planned for future implementation.

## Usage

### Using the Default Provider

```python
from app.services.data_providers import DataProviderFactory

# Create provider instance (uses 'mock' by default)
provider = DataProviderFactory.create()

# Populate data
result = provider.populate_data(db, team_id=1, project_id=1)
```

### Switching Providers

```python
# Option 1: Set default provider globally
DataProviderFactory.set_default('t1')  # Once implemented

# Option 2: Request specific provider
provider = DataProviderFactory.create('github')  # Once implemented
```

### Available Provider Methods

All providers implement the following methods:

- `fetch_commits(db, team_id, project_id, period_start, period_end)` - Fetch commit data
- `fetch_pull_requests(db, team_id, project_id, period_start, period_end)` - Fetch PR data
- `fetch_code_reviews(db, pull_request_ids, team_id)` - Fetch review data
- `fetch_tasks(db, team_id, project_id, period_start, period_end)` - Fetch task/issue data
- `populate_data(db, team_id, project_id, period_start, period_end)` - High-level method to fetch and store all data

## Implementing a New Provider

To add a new data provider (e.g., for T1 Сфера.Код):

### 1. Create the Provider Class

Create a new file `t1_provider.py` in this directory:

```python
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from .base_provider import BaseDataProvider

class T1DataProvider(BaseDataProvider):
    """Data provider for T1 Сфера.Код API."""
    
    def __init__(self, api_key: str, api_url: str):
        """Initialize with T1 API credentials."""
        self.api_key = api_key
        self.api_url = api_url
        # Initialize T1 API client
        # self.client = T1ApiClient(api_key, api_url)
    
    def fetch_commits(self, db, team_id, project_id, period_start, period_end) -> List[Dict]:
        """Fetch real commits from T1 API."""
        # Call T1 API
        # commits = self.client.get_commits(project_id, period_start, period_end)
        
        # Transform T1 response to our format
        # return [self._transform_commit(c) for c in commits]
        pass
    
    def fetch_pull_requests(self, db, team_id, project_id, period_start, period_end) -> List[Dict]:
        """Fetch real PRs from T1 API."""
        pass
    
    def fetch_code_reviews(self, db, pull_request_ids, team_id) -> List[Dict]:
        """Fetch real reviews from T1 API."""
        pass
    
    def fetch_tasks(self, db, team_id, project_id, period_start, period_end) -> List[Dict]:
        """Fetch real tasks from T1 API."""
        pass
    
    def populate_data(self, db, team_id, project_id, period_start=None, period_end=None) -> Dict:
        """Populate database with real data from T1."""
        # Implement similar to MockDataProvider.populate_data()
        # but using real API calls instead of generating mock data
        pass
```

### 2. Register the Provider

Update `__init__.py`:

```python
from .t1_provider import T1DataProvider

__all__ = [..., 'T1DataProvider']
```

Update `provider_factory.py`:

```python
from .t1_provider import T1DataProvider

class DataProviderFactory:
    _providers = {
        'mock': MockDataProvider,
        't1': T1DataProvider,  # Add here
        # ...
    }
```

### 3. Configure and Use

```python
# In your configuration or environment
from app.services.data_providers import DataProviderFactory, T1DataProvider

# Register with configuration
DataProviderFactory.register_provider('t1', T1DataProvider)

# Set as default
DataProviderFactory.set_default('t1')

# Or use directly
provider = DataProviderFactory.create('t1')
result = provider.populate_data(db, team_id=1, project_id=1)
```

## Data Format Requirements

All providers must return data in the following formats (see `base_provider.py` for detailed documentation):

### Commits
```python
{
    'external_id': str,          # Commit SHA
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
    'time_to_first_review': float,  # hours
    'time_to_merge': float,     # hours
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

### Tasks
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
    'time_in_todo': float,      # hours
    'time_in_development': float,  # hours
    'time_in_review': float,    # hours
    'time_in_testing': float    # hours
}
```

## Configuration

You can configure the default provider through environment variables:

```bash
# .env file
DATA_PROVIDER=mock  # Options: mock, t1, github, gitlab
T1_API_KEY=your_api_key_here
T1_API_URL=https://api.t1-sphere.com
```

Then in your configuration:

```python
# app/core/config.py
class Settings(BaseSettings):
    DATA_PROVIDER: str = "mock"
    T1_API_KEY: Optional[str] = None
    T1_API_URL: Optional[str] = None
```

## Testing

Each provider should include tests:

```python
# tests/test_data_providers.py
def test_mock_provider():
    provider = DataProviderFactory.create('mock')
    assert isinstance(provider, MockDataProvider)
    
def test_t1_provider():
    provider = DataProviderFactory.create('t1')
    assert isinstance(provider, T1DataProvider)
```

## Benefits of This Architecture

1. **Easy to switch providers**: Change one line of code or configuration
2. **Testable**: Mock provider for testing, real provider for production
3. **Extensible**: Add new providers without changing existing code
4. **Type-safe**: All providers implement the same interface
5. **Maintainable**: Clear separation of concerns

## Migration Path

Current: `MockDataProvider` → Future: `T1DataProvider` or any other provider

The migration is seamless - just implement the new provider following the interface, register it, and switch the configuration. No changes needed to consuming code.
