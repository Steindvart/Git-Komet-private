"""
Пакет поставщиков данных для Git-Komet.

Этот пакет содержит различные поставщики данных, которые можно легко заменять:
- MockDataProvider: Генерирует mock-данные для демонстрации (текущая реализация)
- T1DataProvider: Реальная интеграция с T1 Сфера.Код (будет реализовано)
- GitHubDataProvider: Интеграция с GitHub (будет реализовано)
- GitLabDataProvider: Интеграция с GitLab (будет реализовано)
"""

from .base_provider import BaseDataProvider
from .mock_provider import MockDataProvider
from .provider_factory import DataProviderFactory

__all__ = ['BaseDataProvider', 'MockDataProvider', 'DataProviderFactory']
