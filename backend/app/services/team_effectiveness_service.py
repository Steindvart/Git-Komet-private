from typing import Dict, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Team, TeamMember, Commit, PullRequest, Task, TeamMetric
import json


class TeamEffectivenessService:
    """Service for calculating overall team effectiveness scores."""

    @staticmethod
    def calculate_effectiveness_score(
        db: Session,
        team_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Dict:
        """Calculate comprehensive team effectiveness score."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            return None
        
        member_ids = [member.id for member in team.members]
        
        # Get commits by team members
        commits = db.query(Commit).filter(
            Commit.author_id.in_(member_ids),
            Commit.committed_at.between(period_start, period_end)
        ).all()
        
        # Get pull requests by team members
        prs = db.query(PullRequest).filter(
            PullRequest.author_id.in_(member_ids),
            PullRequest.created_at.between(period_start, period_end)
        ).all()
        
        # Get tasks assigned to team
        tasks = db.query(Task).filter(
            Task.assignee_id.in_(member_ids),
            Task.created_at.between(period_start, period_end)
        ).all()
        
        # Calculate metrics
        total_commits = len(commits)
        total_prs = len(prs)
        active_contributors = len(set(c.author_id for c in commits if c.author_id))
        
        # Average PR review time
        pr_review_times = [pr.time_to_first_review for pr in prs if pr.time_to_first_review]
        avg_pr_review_time = sum(pr_review_times) / len(pr_review_times) if pr_review_times else 0
        
        # Calculate effectiveness score (0-100)
        # Higher is better
        score_components = []
        
        # 1. Commit activity (max 25 points)
        commit_score = min(25, (total_commits / max(len(member_ids), 1)) * 5)
        score_components.append(commit_score)
        
        # 2. PR throughput (max 25 points)
        pr_score = min(25, (total_prs / max(len(member_ids), 1)) * 10)
        score_components.append(pr_score)
        
        # 3. Review efficiency (max 25 points) - faster is better
        if avg_pr_review_time > 0:
            review_score = max(0, 25 - (avg_pr_review_time / 24) * 5)  # Penalty for slow reviews
        else:
            review_score = 15
        score_components.append(review_score)
        
        # 4. Team collaboration (max 25 points)
        collab_score = (active_contributors / max(len(member_ids), 1)) * 25
        score_components.append(collab_score)
        
        effectiveness_score = sum(score_components)
        
        # Determine trend (simplified - would compare with previous period)
        trend = "stable"
        
        # Check for alerts
        has_alert = False
        alert_message = None
        alert_severity = None
        
        if effectiveness_score < 40:
            has_alert = True
            alert_message = "Team effectiveness is below target. Review bottlenecks and team capacity."
            alert_severity = "critical"
        elif effectiveness_score < 60:
            has_alert = True
            alert_message = "Team effectiveness could be improved. Consider process optimization."
            alert_severity = "warning"
        elif avg_pr_review_time > 48:
            has_alert = True
            alert_message = "PR review times are high. Consider increasing reviewer availability."
            alert_severity = "warning"
        
        return {
            "team_id": team_id,
            "team_name": team.name,
            "effectiveness_score": round(effectiveness_score, 2),
            "trend": trend,
            "total_commits": total_commits,
            "total_prs": total_prs,
            "avg_pr_review_time": round(avg_pr_review_time, 2),
            "active_contributors": active_contributors,
            "has_alert": has_alert,
            "alert_message": alert_message,
            "alert_severity": alert_severity,
            "period_start": period_start,
            "period_end": period_end,
        }

    @staticmethod
    def save_team_metric(
        db: Session,
        team_id: int,
        metric_type: str,
        metric_data: Dict,
        score: float,
        trend: str,
        period_start: datetime,
        period_end: datetime,
        has_alert: bool = False,
        alert_message: str = None,
        alert_severity: str = None
    ) -> TeamMetric:
        """Save team effectiveness metric to database."""
        metric = TeamMetric(
            team_id=team_id,
            metric_type=metric_type,
            metric_value=json.dumps(metric_data),
            score=score,
            trend=trend,
            period_start=period_start,
            period_end=period_end,
            has_alert=has_alert,
            alert_message=alert_message,
            alert_severity=alert_severity
        )
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return metric
