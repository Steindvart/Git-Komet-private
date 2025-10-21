"""
Data provider factory for Git-Komet.

This factory allows easy configuration and switching between different data providers.
"""

from typing import Optional
from .base_provider import BaseDataProvider
from .mock_provider import MockDataProvider


class DataProviderFactory:
    """
    Factory for creating data provider instances.
    
    This makes it easy to switch between mock and real data providers
    through configuration.
    """
    
    # Registry of available providers
    _providers = {
        'mock': MockDataProvider,
        # Future providers can be registered here:
        # 't1': T1DataProvider,
        # 'github': GitHubDataProvider,
        # 'gitlab': GitLabDataProvider,
    }
    
    # Default provider type
    _default_provider = 'mock'
    
    @classmethod
    def create(cls, provider_type: Optional[str] = None) -> BaseDataProvider:
        """
        Create and return a data provider instance.
        
        Args:
            provider_type: Type of provider to create ('mock', 't1', 'github', 'gitlab')
                          If None, uses the default provider.
        
        Returns:
            An instance of the requested data provider.
        
        Raises:
            ValueError: If the provider type is not recognized.
        
        Example:
            # Get the default (mock) provider
            provider = DataProviderFactory.create()
            
            # Get a specific provider
            provider = DataProviderFactory.create('mock')
            
            # In the future, when real providers are implemented:
            provider = DataProviderFactory.create('t1')
        """
        provider_type = provider_type or cls._default_provider
        
        if provider_type not in cls._providers:
            available = ', '.join(cls._providers.keys())
            raise ValueError(
                f"Unknown provider type: {provider_type}. "
                f"Available providers: {available}"
            )
        
        provider_class = cls._providers[provider_type]
        return provider_class()
    
    @classmethod
    def set_default(cls, provider_type: str) -> None:
        """
        Set the default provider type.
        
        Args:
            provider_type: Type of provider to use as default.
        
        Raises:
            ValueError: If the provider type is not recognized.
        """
        if provider_type not in cls._providers:
            available = ', '.join(cls._providers.keys())
            raise ValueError(
                f"Unknown provider type: {provider_type}. "
                f"Available providers: {available}"
            )
        
        cls._default_provider = provider_type
    
    @classmethod
    def register_provider(cls, name: str, provider_class: type) -> None:
        """
        Register a new data provider.
        
        This allows plugins or extensions to add new provider types.
        
        Args:
            name: Name to register the provider under.
            provider_class: The provider class to register.
        
        Example:
            # Register a custom provider
            class CustomProvider(BaseDataProvider):
                ...
            
            DataProviderFactory.register_provider('custom', CustomProvider)
            provider = DataProviderFactory.create('custom')
        """
        if not issubclass(provider_class, BaseDataProvider):
            raise ValueError(
                f"Provider class must inherit from BaseDataProvider"
            )
        
        cls._providers[name] = provider_class
    
    @classmethod
    def get_available_providers(cls) -> list:
        """
        Get list of available provider types.
        
        Returns:
            List of provider type names.
        """
        return list(cls._providers.keys())
