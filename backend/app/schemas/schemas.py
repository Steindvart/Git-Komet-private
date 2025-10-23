from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


# Project Schemas (replaces Repository)
class ProjectBase(BaseModel):
    name: str
    external_id: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Project Member Schemas
class ProjectMemberBase(BaseModel):
    email: str
    name: str
    role: Optional[str] = None


class ProjectMemberCreate(ProjectMemberBase):
    project_id: int


class ProjectMember(ProjectMemberBase):
    id: int
    project_id: int
    joined_at: datetime

    class Config:
        from_attributes = True


# Commit Schemas
class CommitBase(BaseModel):
    external_id: str
    message: str
    author_email: str
    author_name: str
    committed_at: datetime
    files_changed: int = 0
    insertions: int = 0
    deletions: int = 0
    has_tests: bool = False
    test_coverage_delta: Optional[float] = None
    todo_count: int = 0


class Commit(CommitBase):
    id: int
    author_id: Optional[int] = None

    class Config:
        from_attributes = True


# Pull Request Schemas
class PullRequestBase(BaseModel):
    external_id: str
    project_id: int
    title: str
    description: Optional[str] = None
    state: str
    created_at: datetime
    updated_at: datetime


class PullRequest(PullRequestBase):
    id: int
    author_id: Optional[int] = None
    merged_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    time_to_first_review: Optional[float] = None
    time_to_merge: Optional[float] = None
    review_cycles: int = 0
    lines_added: int = 0
    lines_deleted: int = 0
    files_changed: int = 0

    class Config:
        from_attributes = True


# Code Review Schemas
class CodeReviewBase(BaseModel):
    pull_request_id: int
    state: str
    created_at: datetime
    comments_count: int = 0
    critical_comments: int = 0


class CodeReview(CodeReviewBase):
    id: int
    reviewer_id: Optional[int] = None

    class Config:
        from_attributes = True


# Task Schemas
class TaskBase(BaseModel):
    external_id: str
    project_id: int
    title: str
    description: Optional[str] = None
    state: str
    priority: Optional[str] = None
    created_at: datetime


class Task(TaskBase):
    id: int
    assignee_id: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    time_in_todo: Optional[float] = None
    time_in_development: Optional[float] = None
    time_in_review: Optional[float] = None
    time_in_testing: Optional[float] = None

    class Config:
        from_attributes = True


# Analysis Response Schemas
class ProjectEffectivenessMetrics(BaseModel):
    """
    Метрики эффективности проекта / Project effectiveness metrics.
    
    Новое ТЗ: Метрики основаны только на данных коммитов.
    """
    project_id: int
    project_name: str
    effectiveness_score: float  # 0-100
    trend: str  # improving, stable, declining
    total_commits: int
    active_contributors: int
    after_hours_percentage: float
    weekend_percentage: float
    churn_rate: float
    has_alert: bool
    alert_message: Optional[str] = None
    alert_severity: Optional[str] = None
    period_start: datetime
    period_end: datetime


class EmployeeCareMetrics(BaseModel):
    """Метрика заботы о сотрудниках / Employee care metrics"""
    project_id: int
    project_name: str
    employee_care_score: float  # 0-100, higher is better
    after_hours_percentage: float
    weekend_percentage: float
    status: str  # excellent, good, needs_attention, critical
    recommendations: List[str]
    period_start: datetime
    period_end: datetime


class ActiveContributorsMetrics(BaseModel):
    """
    Метрика активных участников / Active contributors metrics.
    
    Новое ТЗ: Анализ активных участников - количество уникальных авторов коммитов
    за период, чтобы понимать сколько человеческих ресурсов тратится на проект.
    """
    project_id: int
    project_name: str
    active_contributors: int
    total_commits: int
    avg_commits_per_contributor: float
    period_start: datetime
    period_end: datetime


class ContributorCommitStats(BaseModel):
    """Статистика коммитов отдельного участника / Individual contributor commit stats"""
    author_id: int
    author_name: str
    author_email: str
    commit_count: int
    lines_changed: int
    expertise_level: str  # beginner, intermediate, advanced, expert


class CommitsPerPersonMetrics(BaseModel):
    """
    Метрика коммитов на человека / Commits per person metrics.
    
    Новое ТЗ: Количество коммитов на участника для понимания уровня экспертности по проекту.
    """
    project_id: int
    project_name: str
    contributors: List[ContributorCommitStats]
    total_contributors: int
    period_start: datetime
    period_end: datetime


class TechnicalDebtAnalysis(BaseModel):
    """
    Анализ технического долга на основе TODO комментариев.
    Technical debt analysis based on TODO comments only.
    
    Новое ТЗ: Анализируются ТОЛЬКО TODO комментарии из diff коммитов.
    """
    project_id: int
    todo_count: int
    todo_trend: str  # up, down, stable
    technical_debt_score: float  # 0-100, lower is better
    recommendations: List[str]
    period_start: datetime
    period_end: datetime


class BottleneckAnalysis(BaseModel):
    team_id: Optional[int] = None
    project_id: Optional[int] = None
    bottleneck_stage: str  # review, development, testing, todo, none
    avg_time_in_stage: float  # hours
    affected_tasks_count: int
    impact_score: float  # 0-100
    recommendations: List[str]
    stage_times: Optional[dict] = None
    period_start: datetime
    period_end: datetime


class PRNeedingAttention(BaseModel):
    """PR/MR, требующий внимания / PR/MR needing attention"""
    pr_id: int
    external_id: str
    title: str
    author_id: Optional[int] = None
    created_at: datetime
    time_in_review_hours: float
    indicator: str  # ☀️, 🌧️, 🌩️
    has_reviews: bool
    review_cycles: int


class PRsNeedingAttentionResponse(BaseModel):
    """Ответ со списком PR/MR, требующих внимания / Response with list of PRs needing attention"""
    project_id: int
    prs: List[PRNeedingAttention]
    total_count: int
