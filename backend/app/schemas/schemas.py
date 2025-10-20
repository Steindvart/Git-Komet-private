from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional, List


# Repository Schemas
class RepositoryBase(BaseModel):
    name: str
    url: str
    description: Optional[str] = None


class RepositoryCreate(RepositoryBase):
    pass


class RepositoryUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    description: Optional[str] = None


class Repository(RepositoryBase):
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
    sha: str
    message: str
    author_email: str
    author_name: str
    committed_at: datetime
    files_changed: int = 0
    insertions: int = 0
    deletions: int = 0


class Commit(CommitBase):
    id: int
    repository_id: int
    author_id: Optional[int] = None

    class Config:
        from_attributes = True


# Metric Schemas
class MetricBase(BaseModel):
    metric_type: str
    metric_value: str
    period_start: datetime
    period_end: datetime


class MetricCreate(MetricBase):
    repository_id: int


class Metric(MetricBase):
    id: int
    repository_id: int
    calculated_at: datetime

    class Config:
        from_attributes = True


# Analysis Response Schemas
class TeamEffectivenessMetrics(BaseModel):
    team_id: int
    team_name: str
    total_commits: int
    total_lines_changed: int
    commit_frequency: float
    avg_commit_size: float
    active_contributors: int
    period_start: datetime
    period_end: datetime


class RepositoryMetrics(BaseModel):
    repository_id: int
    repository_name: str
    total_commits: int
    total_contributors: int
    commit_frequency: float
    code_churn: float
    period_start: datetime
    period_end: datetime
