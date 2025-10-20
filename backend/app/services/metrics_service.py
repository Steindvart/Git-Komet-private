from typing import Dict, List
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Commit, Repository, Team, TeamMember, Metric
import json


class MetricsService:
    """Service for calculating team and repository metrics."""

    @staticmethod
    def calculate_team_effectiveness(
        db: Session,
        team_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Dict:
        """Calculate team effectiveness metrics."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            return None
        
        # Get team member emails
        member_emails = [member.email for member in team.members]
        
        # Get commits by team members in the period
        commits = db.query(Commit).filter(
            Commit.author_email.in_(member_emails),
            Commit.committed_at.between(period_start, period_end)
        ).all()
        
        if not commits:
            return {
                "team_id": team_id,
                "team_name": team.name,
                "total_commits": 0,
                "total_lines_changed": 0,
                "commit_frequency": 0.0,
                "avg_commit_size": 0.0,
                "active_contributors": 0,
                "period_start": period_start,
                "period_end": period_end,
            }
        
        total_commits = len(commits)
        total_lines = sum(c.insertions + c.deletions for c in commits)
        active_contributors = len(set(c.author_email for c in commits))
        days = (period_end - period_start).days or 1
        
        return {
            "team_id": team_id,
            "team_name": team.name,
            "total_commits": total_commits,
            "total_lines_changed": total_lines,
            "commit_frequency": total_commits / days,
            "avg_commit_size": total_lines / total_commits if total_commits > 0 else 0,
            "active_contributors": active_contributors,
            "period_start": period_start,
            "period_end": period_end,
        }

    @staticmethod
    def calculate_repository_metrics(
        db: Session,
        repository_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Dict:
        """Calculate repository metrics."""
        repository = db.query(Repository).filter(Repository.id == repository_id).first()
        if not repository:
            return None
        
        commits = db.query(Commit).filter(
            Commit.repository_id == repository_id,
            Commit.committed_at.between(period_start, period_end)
        ).all()
        
        if not commits:
            return {
                "repository_id": repository_id,
                "repository_name": repository.name,
                "total_commits": 0,
                "total_contributors": 0,
                "commit_frequency": 0.0,
                "code_churn": 0.0,
                "period_start": period_start,
                "period_end": period_end,
            }
        
        total_commits = len(commits)
        contributors = len(set(c.author_email for c in commits))
        days = (period_end - period_start).days or 1
        total_changes = sum(c.insertions + c.deletions for c in commits)
        
        return {
            "repository_id": repository_id,
            "repository_name": repository.name,
            "total_commits": total_commits,
            "total_contributors": contributors,
            "commit_frequency": total_commits / days,
            "code_churn": total_changes / total_commits if total_commits > 0 else 0,
            "period_start": period_start,
            "period_end": period_end,
        }

    @staticmethod
    def save_metric(
        db: Session,
        repository_id: int,
        metric_type: str,
        metric_value: Dict,
        period_start: datetime,
        period_end: datetime
    ) -> Metric:
        """Save calculated metric to database."""
        metric = Metric(
            repository_id=repository_id,
            metric_type=metric_type,
            metric_value=json.dumps(metric_value),
            period_start=period_start,
            period_end=period_end
        )
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return metric
