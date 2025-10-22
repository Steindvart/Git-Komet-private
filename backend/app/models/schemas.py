from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ProjectBase(BaseModel):
    """Базовая схема проекта"""
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Схема для создания проекта"""
    pass


class ProjectResponse(ProjectBase):
    """Схема ответа с информацией о проекте"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PullRequestBase(BaseModel):
    """Базовая схема Pull Request"""
    pr_number: int
    title: str
    author: str
    created_at: datetime
    merged_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    first_review_at: Optional[datetime] = None
    approved_at: Optional[datetime] = None


class PullRequestCreate(PullRequestBase):
    """Схема для создания Pull Request"""
    project_id: int


class PullRequestResponse(PullRequestBase):
    """Схема ответа с информацией о Pull Request"""
    id: int
    project_id: int

    class Config:
        from_attributes = True


class IssueBase(BaseModel):
    """Базовая схема задачи"""
    issue_number: int
    title: str
    author: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    status: str = "open"


class IssueCreate(IssueBase):
    """Схема для создания задачи"""
    project_id: int


class IssueResponse(IssueBase):
    """Схема ответа с информацией о задаче"""
    id: int
    project_id: int

    class Config:
        from_attributes = True


class MetricResponse(BaseModel):
    """Схема ответа с метрикой"""
    id: int
    project_id: int
    metric_type: str
    metric_name: str
    value: float
    calculated_at: datetime

    class Config:
        from_attributes = True


class BottleneckAnalysis(BaseModel):
    """Схема анализа узких мест"""
    project_id: int
    project_name: str
    avg_pr_review_time_hours: Optional[float] = Field(None, description="Среднее время на ревью PR (часы)")
    avg_pr_approval_time_hours: Optional[float] = Field(None, description="Среднее время до одобрения PR (часы)")
    avg_pr_merge_time_hours: Optional[float] = Field(None, description="Среднее время до мерджа PR (часы)")
    avg_issue_start_time_hours: Optional[float] = Field(None, description="Среднее время до начала работы над задачей (часы)")
    avg_issue_completion_time_hours: Optional[float] = Field(None, description="Среднее время выполнения задачи (часы)")
    total_prs: int = Field(0, description="Общее количество PR")
    total_issues: int = Field(0, description="Общее количество задач")
    bottlenecks: List[str] = Field(default_factory=list, description="Список обнаруженных узких мест")
    recommendations: List[str] = Field(default_factory=list, description="Рекомендации по улучшению")
