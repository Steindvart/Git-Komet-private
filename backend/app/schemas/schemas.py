from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict


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


# Team Schemas
class TeamMemberBase(BaseModel):
    email: str
    name: str
    role: Optional[str] = None


class TeamMemberCreate(TeamMemberBase):
    team_id: int


class TeamMember(TeamMemberBase):
    id: int
    team_id: int
    joined_at: datetime

    class Config:
        from_attributes = True


class TeamBase(BaseModel):
    name: str
    description: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int
    created_at: datetime
    members: List[TeamMember] = []

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
class TeamEffectivenessMetrics(BaseModel):
    team_id: int
    team_name: str
    effectiveness_score: float  # 0-100
    trend: str  # improving, stable, declining
    total_commits: int
    total_prs: int
    avg_pr_review_time: float
    active_contributors: int
    after_hours_percentage: float
    weekend_percentage: float
    churn_rate: float
    has_alert: bool
    alert_message: Optional[str] = None
    alert_severity: Optional[str] = None
    period_start: str  # ISO format datetime string
    period_end: str  # ISO format datetime string


class TechnicalDebtAnalysis(BaseModel):
    team_id: Optional[int] = None
    project_id: Optional[int] = None
    test_coverage: float
    test_coverage_trend: str
    todo_count_code: int
    todo_count_reviews: int
    todo_trend: str
    review_comment_density: float
    churn_rate: float
    technical_debt_score: float  # 0-100, lower is better
    recommendations: List[str]
    period_start: str  # ISO format datetime string
    period_end: str  # ISO format datetime string


class BottleneckAnalysis(BaseModel):
    team_id: int
    bottleneck_stage: str  # review, development, testing
    avg_time_in_stage: float  # hours
    affected_tasks_count: int
    impact_score: float  # 0-100
    recommendations: List[str]
    stage_breakdown: Dict  # Dictionary with stage details
    period_start: str  # ISO format datetime string
    period_end: str  # ISO format datetime string
