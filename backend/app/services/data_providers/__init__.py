"""
Data providers package for Git-Komet.

This package contains different data providers that can be easily swapped:
- MockDataProvider: Generates mock data for demonstration (current implementation)
- T1DataProvider: Real integration with T1 Сфера.Код (to be implemented)
- GitHubDataProvider: Integration with GitHub (to be implemented)
- GitLabDataProvider: Integration with GitLab (to be implemented)
"""

from .base_provider import BaseDataProvider
from .mock_provider import MockDataProvider
from .provider_factory import DataProviderFactory

__all__ = ['BaseDataProvider', 'MockDataProvider', 'DataProviderFactory']
