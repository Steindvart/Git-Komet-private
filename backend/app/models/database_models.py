from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Project(Base):
    """Модель проекта"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    pull_requests = relationship("PullRequest", back_populates="project")
    issues = relationship("Issue", back_populates="project")


class PullRequest(Base):
    """Модель Pull Request/Merge Request"""
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    pr_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    merged_at = Column(DateTime)
    closed_at = Column(DateTime)
    first_review_at = Column(DateTime)
    approved_at = Column(DateTime)
    
    # Relationships
    project = relationship("Project", back_populates="pull_requests")


class Issue(Base):
    """Модель задачи/Issue"""
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    issue_number = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    closed_at = Column(DateTime)
    status = Column(String, default="open")  # open, in_progress, completed, closed
    
    # Relationships
    project = relationship("Project", back_populates="issues")


class Metric(Base):
    """Модель для хранения вычисленных метрик проекта"""
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    metric_type = Column(String, nullable=False)  # pr_review_time, issue_completion_time, etc.
    metric_name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    project = relationship("Project")
