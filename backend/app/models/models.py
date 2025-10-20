from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.session import Base


class Project(Base):
    """Project from T1 Сфера.Код - represents a project/repository"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)  # ID from T1 API
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    pull_requests = relationship("PullRequest", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")
    team_metrics = relationship("TeamMetric", back_populates="team", cascade="all, delete-orphan")


class TeamMember(Base):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    external_id = Column(String, index=True, nullable=True)  # ID from T1 API
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    team = relationship("Team", back_populates="members")
    commits = relationship("Commit", back_populates="author")
    pull_requests = relationship("PullRequest", foreign_keys="PullRequest.author_id", back_populates="author")
    reviews = relationship("CodeReview", back_populates="reviewer")
    tasks = relationship("Task", back_populates="assignee")


class Commit(Base):
    """Commit data from T1 Сфера.Код"""
    __tablename__ = "commits"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)  # SHA from T1 API
    author_id = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    message = Column(String, nullable=False)
    author_email = Column(String, nullable=False)
    author_name = Column(String, nullable=False)
    committed_at = Column(DateTime, nullable=False)
    files_changed = Column(Integer, default=0)
    insertions = Column(Integer, default=0)
    deletions = Column(Integer, default=0)
    has_tests = Column(Boolean, default=False)
    test_coverage_delta = Column(Float, nullable=True)  # Change in test coverage
    todo_count = Column(Integer, default=0)  # Number of TODO comments added
    
    # Code churn tracking
    is_churn = Column(Boolean, default=False)  # If code was modified again within short period
    churn_days = Column(Integer, nullable=True)  # Days since last modification of same files
    
    # Work-life balance tracking
    is_after_hours = Column(Boolean, default=False)  # Committed outside working hours
    is_weekend = Column(Boolean, default=False)  # Committed on weekend
    
    # Relationships
    author = relationship("TeamMember", back_populates="commits")


class PullRequest(Base):
    """Pull Request data from T1 Сфера.Код"""
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)  # ID from T1 API
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    state = Column(String, nullable=False)  # open, merged, closed
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    merged_at = Column(DateTime, nullable=True)
    closed_at = Column(DateTime, nullable=True)
    
    # Time tracking
    time_to_first_review = Column(Float, nullable=True)  # Hours
    time_to_merge = Column(Float, nullable=True)  # Hours
    review_cycles = Column(Integer, default=0)
    
    # Code metrics
    lines_added = Column(Integer, default=0)
    lines_deleted = Column(Integer, default=0)
    files_changed = Column(Integer, default=0)
    
    # Relationships
    project = relationship("Project", back_populates="pull_requests")
    author = relationship("TeamMember", foreign_keys=[author_id], back_populates="pull_requests")
    reviews = relationship("CodeReview", back_populates="pull_request", cascade="all, delete-orphan")


class CodeReview(Base):
    """Code Review data from T1 Сфера.Код"""
    __tablename__ = "code_reviews"

    id = Column(Integer, primary_key=True, index=True)
    pull_request_id = Column(Integer, ForeignKey("pull_requests.id"), nullable=False)
    reviewer_id = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    state = Column(String, nullable=False)  # approved, changes_requested, commented
    created_at = Column(DateTime, nullable=False)
    comments_count = Column(Integer, default=0)
    critical_comments = Column(Integer, default=0)  # Number of critical/blocking comments
    todo_comments = Column(Integer, default=0)  # Number of TODO suggestions in review
    
    # Relationships
    pull_request = relationship("PullRequest", back_populates="reviews")
    reviewer = relationship("TeamMember", back_populates="reviews")


class Task(Base):
    """Task/Issue data from T1 Сфера.Код"""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(String, unique=True, index=True, nullable=False)  # ID from T1 API
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("team_members.id"), nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    state = Column(String, nullable=False)  # todo, in_progress, in_review, done
    priority = Column(String, nullable=True)  # low, medium, high, critical
    
    created_at = Column(DateTime, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Time tracking for bottleneck analysis
    time_in_todo = Column(Float, nullable=True)  # Hours
    time_in_development = Column(Float, nullable=True)  # Hours
    time_in_review = Column(Float, nullable=True)  # Hours
    time_in_testing = Column(Float, nullable=True)  # Hours
    
    # Relationships
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("TeamMember", back_populates="tasks")


class TeamMetric(Base):
    """Calculated team effectiveness metrics"""
    __tablename__ = "team_metrics"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    metric_type = Column(String, nullable=False)  # effectiveness_score, technical_debt, bottleneck, etc.
    metric_value = Column(String, nullable=False)  # JSON string for complex values
    score = Column(Float, nullable=True)  # Normalized score 0-100
    trend = Column(String, nullable=True)  # improving, stable, declining
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Alert data
    has_alert = Column(Boolean, default=False)
    alert_message = Column(String, nullable=True)
    alert_severity = Column(String, nullable=True)  # info, warning, critical
    
    # Relationships
    team = relationship("Team", back_populates="team_metrics")


class TechnicalDebtMetric(Base):
    """Technical debt tracking over time"""
    __tablename__ = "technical_debt_metrics"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    
    # Metrics
    test_coverage = Column(Float, nullable=True)  # Percentage
    test_coverage_trend = Column(String, nullable=True)  # up, down, stable
    todo_count = Column(Integer, default=0)
    todo_trend = Column(String, nullable=True)
    review_comment_density = Column(Float, nullable=True)  # Comments per PR
    
    measured_at = Column(DateTime, nullable=False)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
