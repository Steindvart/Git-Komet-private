"""
Фабрика поставщиков данных для Git-Komet.

Эта фабрика позволяет легко настраивать и переключаться между различными поставщиками данных.
"""

from typing import Optional
from .base_provider import BaseDataProvider
from .mock_provider import MockDataProvider


class DataProviderFactory:
    """
    Фабрика для создания экземпляров поставщиков данных.
    
    Упрощает переключение между mock и реальными поставщиками данных
    через конфигурацию.
    """
    
    # Реестр доступных поставщиков
    _providers = {
        'mock': MockDataProvider,
        # Будущие поставщики могут быть зарегистрированы здесь:
        # 't1': T1DataProvider,
        # 'github': GitHubDataProvider,
        # 'gitlab': GitLabDataProvider,
    }
    
    # Тип поставщика по умолчанию
    _default_provider = 'mock'
    
    @classmethod
    def create(cls, provider_type: Optional[str] = None) -> BaseDataProvider:
        """
        Создать и вернуть экземпляр поставщика данных.
        
        Args:
            provider_type: Тип создаваемого поставщика ('mock', 't1', 'github', 'gitlab')
                          Если None, использует поставщика по умолчанию.
        
        Returns:
            Экземпляр запрошенного поставщика данных.
        
        Raises:
            ValueError: Если тип поставщика не распознан.
        
        Пример:
            # Получить поставщика по умолчанию (mock)
            provider = DataProviderFactory.create()
            
            # Получить конкретного поставщика
            provider = DataProviderFactory.create('mock')
            
            # В будущем, когда реальные поставщики будут реализованы:
            provider = DataProviderFactory.create('t1')
        """
        provider_type = provider_type or cls._default_provider
        
        if provider_type not in cls._providers:
            available = ', '.join(cls._providers.keys())
            raise ValueError(
                f"Неизвестный тип поставщика: {provider_type}. "
                f"Доступные поставщики: {available}"
            )
        
        provider_class = cls._providers[provider_type]
        return provider_class()
    
    @classmethod
    def set_default(cls, provider_type: str) -> None:
        """
        Установить тип поставщика по умолчанию.
        
        Args:
            provider_type: Тип поставщика для использования по умолчанию.
        
        Raises:
            ValueError: Если тип поставщика не распознан.
        """
        if provider_type not in cls._providers:
            available = ', '.join(cls._providers.keys())
            raise ValueError(
                f"Неизвестный тип поставщика: {provider_type}. "
                f"Доступные поставщики: {available}"
            )
        
        cls._default_provider = provider_type
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type) -> None:
        """
        Зарегистрировать нового поставщика данных.
        
        Это позволяет плагинам или расширениям добавлять новые типы поставщиков.
        
        Args:
            name: Имя для регистрации поставщика.
            provider_class: Класс поставщика для регистрации.
        
        Пример:
            # Зарегистрировать пользовательского поставщика
            class CustomProvider(BaseDataProvider):
                ...
            
            DataProviderFactory.register_provider('custom', CustomProvider)
            provider = DataProviderFactory.create('custom')
        """
        if not issubclass(provider_class, BaseDataProvider):
            raise ValueError(
                f"Класс поставщика должен наследоваться от BaseDataProvider"
            )
        
        cls._providers[name] = provider_class
    
    @classmethod
    def get_available_providers(cls) -> list:
        """
        Получить список доступных типов поставщиков.
        
        Returns:
            Список имен типов поставщиков.
        """
        return list(cls._providers.keys())
