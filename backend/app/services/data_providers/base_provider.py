"""
Base data provider interface.

This defines the contract that all data providers must implement,
making it easy to swap between mock and real data sources.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session


class BaseDataProvider(ABC):
    """Base interface for all data providers."""
    
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
        Fetch commit data from the data source.
        
        Returns a list of commit dictionaries with the following structure:
        - external_id: str (commit SHA)
        - author_email: str
        - author_name: str
        - message: str
        - committed_at: datetime
        - files_changed: int
        - insertions: int
        - deletions: int
        - has_tests: bool
        - test_coverage_delta: float (optional)
        - todo_count: int
        - is_churn: bool
        - churn_days: int (optional)
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
        Fetch pull request data from the data source.
        
        Returns a list of PR dictionaries with the following structure:
        - external_id: str
        - project_id: int
        - author_email: str
        - title: str
        - description: str (optional)
        - state: str (open, merged, closed)
        - created_at: datetime
        - updated_at: datetime
        - merged_at: datetime (optional)
        - time_to_first_review: float (hours, optional)
        - time_to_merge: float (hours, optional)
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
        Fetch code review data from the data source.
        
        Returns a list of review dictionaries with the following structure:
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
        Fetch task/issue data from the data source.
        
        Returns a list of task dictionaries with the following structure:
        - external_id: str
        - project_id: int
        - assignee_email: str
        - title: str
        - description: str (optional)
        - state: str (todo, in_progress, in_review, done)
        - priority: str (low, medium, high, critical)
        - created_at: datetime
        - started_at: datetime (optional)
        - completed_at: datetime (optional)
        - time_in_todo: float (hours, optional)
        - time_in_development: float (hours, optional)
        - time_in_review: float (hours, optional)
        - time_in_testing: float (hours, optional)
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
        Populate database with data from the source.
        
        This is a high-level method that orchestrates fetching and storing
        all types of data (commits, PRs, reviews, tasks).
        
        Returns a dictionary with counts of created records:
        - commits_created: int
        - pull_requests_created: int
        - reviews_created: int
        - tasks_created: int
        - message: str
        """
        pass
