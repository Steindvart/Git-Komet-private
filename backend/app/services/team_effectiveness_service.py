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
        period_end: datetime,
        project_id: int = None
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
        pr_query = db.query(PullRequest).filter(
            PullRequest.author_id.in_(member_ids),
            PullRequest.created_at.between(period_start, period_end)
        )
        if project_id:
            pr_query = pr_query.filter(PullRequest.project_id == project_id)
        prs = pr_query.all()
        
        # Get tasks assigned to team
        task_query = db.query(Task).filter(
            Task.assignee_id.in_(member_ids),
            Task.created_at.between(period_start, period_end)
        )
        if project_id:
            task_query = task_query.filter(Task.project_id == project_id)
        tasks = task_query.all()
        
        # Calculate metrics
        total_commits = len(commits)
        total_prs = len(prs)
        active_contributors = len(set(c.author_id for c in commits if c.author_id))
        
        # Average PR review time
        pr_review_times = [pr.time_to_first_review for pr in prs if pr.time_to_first_review]
        avg_pr_review_time = sum(pr_review_times) / len(pr_review_times) if pr_review_times else 0
        
        # Work-life balance metrics
        after_hours_commits = [c for c in commits if c.is_after_hours]
        weekend_commits = [c for c in commits if c.is_weekend]
        after_hours_percentage = (len(after_hours_commits) / total_commits * 100) if total_commits > 0 else 0
        weekend_percentage = (len(weekend_commits) / total_commits * 100) if total_commits > 0 else 0
        
        # Code churn metrics
        churn_commits = [c for c in commits if c.is_churn]
        churn_rate = (len(churn_commits) / total_commits * 100) if total_commits > 0 else 0
        
        # Calculate effectiveness score (0-100)
        # Higher is better
        score_components = []
        
        # 1. Commit activity (max 20 points)
        commit_score = min(20, (total_commits / max(len(member_ids), 1)) * 4)
        score_components.append(commit_score)
        
        # 2. PR throughput (max 20 points)
        pr_score = min(20, (total_prs / max(len(member_ids), 1)) * 8)
        score_components.append(pr_score)
        
        # 3. Review efficiency (max 20 points) - faster is better
        if avg_pr_review_time > 0:
            review_score = max(0, 20 - (avg_pr_review_time / 24) * 4)  # Penalty for slow reviews
        else:
            review_score = 12
        score_components.append(review_score)
        
        # 4. Team collaboration (max 20 points)
        collab_score = (active_contributors / max(len(member_ids), 1)) * 20
        score_components.append(collab_score)
        
        # 5. Work-life balance (max 10 points) - penalize overwork
        if after_hours_percentage > 30 or weekend_percentage > 20:
            work_life_score = max(0, 10 - (after_hours_percentage / 10))
        else:
            work_life_score = 10
        score_components.append(work_life_score)
        
        # 6. Code quality (max 10 points) - penalize high churn
        if churn_rate > 25:
            quality_score = max(0, 10 - (churn_rate / 10))
        else:
            quality_score = 10
        score_components.append(quality_score)
        
        effectiveness_score = sum(score_components)
        
        # Determine trend (simplified - would compare with previous period)
        trend = "stable"
        
        # Check for alerts
        has_alert = False
        alert_message = None
        alert_severity = None
        
        if effectiveness_score < 40:
            has_alert = True
            alert_message = "Эффективность команды ниже целевого уровня. Проверьте узкие места и загруженность команды."
            alert_severity = "critical"
        elif effectiveness_score < 60:
            has_alert = True
            alert_message = "Эффективность команды может быть улучшена. Рассмотрите оптимизацию процессов."
            alert_severity = "warning"
        elif avg_pr_review_time > 48:
            has_alert = True
            alert_message = "Время ревью PR слишком велико. Рассмотрите увеличение доступности ревьюеров."
            alert_severity = "warning"
        elif after_hours_percentage > 30:
            has_alert = True
            alert_message = "Обнаружена высокая активность вне рабочего времени. Возможны переработки в команде."
            alert_severity = "warning"
        elif weekend_percentage > 20:
            has_alert = True
            alert_message = "Обнаружена высокая активность в выходные дни. Проверьте нагрузку на команду."
            alert_severity = "warning"
        elif churn_rate > 25:
            has_alert = True
            alert_message = "Высокий уровень переписывания кода. Возможны проблемы с качеством или планированием."
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
            "after_hours_percentage": round(after_hours_percentage, 2),
            "weekend_percentage": round(weekend_percentage, 2),
            "churn_rate": round(churn_rate, 2),
            "has_alert": has_alert,
            "alert_message": alert_message,
            "alert_severity": alert_severity,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
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
