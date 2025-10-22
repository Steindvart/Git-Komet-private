"""
Базовый интерфейс поставщика данных.

Определяет контракт, который должны реализовывать все поставщики данных,
что упрощает переключение между mock и реальными источниками данных.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session


class BaseDataProvider(ABC):
    """Базовый интерфейс для всех поставщиков данных."""
    
    @abstractmethod
    def fetch_commits(
        self,
        db: Session,
        team_id: int,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> List[Dict]:
        """
        Получить данные о коммитах из источника данных.
        
        Возвращает список словарей коммитов со следующей структурой:
        - external_id: str (SHA коммита)
        - author_email: str
        - author_name: str
        - message: str
        - committed_at: datetime
        - files_changed: int
        - insertions: int
        - deletions: int
        - has_tests: bool
        - test_coverage_delta: float (опционально)
        - todo_count: int
        - is_churn: bool
        - churn_days: int (опционально)
        - is_after_hours: bool
        - is_weekend: bool
        """
        pass
    
    @abstractmethod
    def fetch_pull_requests(
        self,
        db: Session,
        team_id: int,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> List[Dict]:
        """
        Получить данные о pull request из источника данных.
        
        Возвращает список словарей PR со следующей структурой:
        - external_id: str
        - project_id: int
        - author_email: str
        - title: str
        - description: str (опционально)
        - state: str (open, merged, closed)
        - created_at: datetime
        - updated_at: datetime
        - merged_at: datetime (опционально)
        - time_to_first_review: float (часы, опционально)
        - time_to_merge: float (часы, опционально)
        - review_cycles: int
        - lines_added: int
        - lines_deleted: int
        - files_changed: int
        """
        pass
    
    @abstractmethod
    def fetch_code_reviews(
        self,
        db: Session,
        pull_request_ids: List[int],
        team_id: int
    ) -> List[Dict]:
        """
        Получить данные о code review из источника данных.
        
        Возвращает список словарей ревью со следующей структурой:
        - pull_request_id: int
        - reviewer_email: str
        - state: str (approved, changes_requested, commented)
        - created_at: datetime
        - comments_count: int
        - critical_comments: int
        - todo_comments: int
        """
        pass
    
    @abstractmethod
    def fetch_tasks(
        self,
        db: Session,
        team_id: int,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> List[Dict]:
        """
        Получить данные о задачах/issues из источника данных.
        
        Возвращает список словарей задач со следующей структурой:
        - external_id: str
        - project_id: int
        - assignee_email: str
        - title: str
        - description: str (опционально)
        - state: str (todo, in_progress, in_review, done)
        - priority: str (low, medium, high, critical)
        - created_at: datetime
        - started_at: datetime (опционально)
        - completed_at: datetime (опционально)
        - time_in_todo: float (часы, опционально)
        - time_in_development: float (часы, опционально)
        - time_in_review: float (часы, опционально)
        - time_in_testing: float (часы, опционально)
        """
        pass
    
    @abstractmethod
    def populate_data(
        self,
        db: Session,
        team_id: int,
        project_id: int,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None
    ) -> Dict:
        """
        Заполнить базу данных данными из источника.
        
        Это высокоуровневый метод, который координирует получение и сохранение
        всех типов данных (коммиты, PR, ревью, задачи).
        
        Возвращает словарь с количеством созданных записей:
        - commits_created: int
        - pull_requests_created: int
        - reviews_created: int
        - tasks_created: int
        - message: str
        """
        pass
