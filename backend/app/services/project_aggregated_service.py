"""
Сервис для расчёта агрегированных метрик эффективности проекта.
Service for calculating aggregated project effectiveness metrics.
"""
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Project, Repository, ProjectMember, Commit, ProjectMetric
from app.services.repository_effectiveness_service import RepositoryEffectivenessService
from app.services.repository_technical_debt_service import RepositoryTechnicalDebtService
import json


def datetime_converter(o):
    """Convert datetime to ISO format string for JSON serialization."""
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError(f"Object of type {type(o)} is not JSON serializable")


class ProjectAggregatedService:
    """Сервис для расчёта агрегированных метрик проекта на основе его репозиториев."""

    @staticmethod
    def calculate_project_metrics(
        db: Session,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Рассчитать агрегированные метрики проекта.
        Calculate aggregated project metrics from all repositories.
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return None
        
        # Получить все репозитории проекта
        repositories = db.query(Repository).filter(Repository.project_id == project_id).all()
        
        if not repositories:
            return {
                "project_id": project_id,
                "project_name": project.name,
                "repository_count": 0,
                "avg_effectiveness_score": 0.0,
                "avg_technical_debt": 0.0,
                "total_active_contributors": 0,
                "trend": "stable",
                "has_alert": False,
                "alert_message": None,
                "alert_severity": None,
                "period_start": period_start,
                "period_end": period_end,
            }
        
        # Собрать метрики по всем репозиториям
        repo_effectiveness_scores = []
        repo_technical_debt_scores = []
        all_contributors = set()
        alerts = []
        
        for repo in repositories:
            # Эффективность репозитория
            effectiveness = RepositoryEffectivenessService.calculate_effectiveness_score(
                db, repo.id, period_start, period_end
            )
            if effectiveness:
                repo_effectiveness_scores.append(effectiveness["effectiveness_score"])
                
                # Собрать активных участников
                commits = db.query(Commit).filter(
                    Commit.repository_id == repo.id,
                    Commit.committed_at.between(period_start, period_end)
                ).all()
                for commit in commits:
                    if commit.author_id:
                        all_contributors.add(commit.author_id)
                
                # Собрать алерты
                if effectiveness["has_alert"]:
                    alerts.append({
                        "repository_name": repo.name,
                        "message": effectiveness["alert_message"],
                        "severity": effectiveness["alert_severity"]
                    })
            
            # Технический долг репозитория
            tech_debt = RepositoryTechnicalDebtService.analyze_technical_debt(
                db, repo.id, period_start, period_end
            )
            if tech_debt:
                repo_technical_debt_scores.append(tech_debt["technical_debt_score"])
        
        # Рассчитать средние значения
        avg_effectiveness_score = sum(repo_effectiveness_scores) / len(repo_effectiveness_scores) if repo_effectiveness_scores else 0.0
        avg_technical_debt = sum(repo_technical_debt_scores) / len(repo_technical_debt_scores) if repo_technical_debt_scores else 0.0
        total_active_contributors = len(all_contributors)
        
        # Определить тренд
        trend = "stable"
        if avg_effectiveness_score >= 80:
            trend = "improving"
        elif avg_effectiveness_score < 50:
            trend = "declining"
        
        # Определить главный алерт проекта
        has_alert = len(alerts) > 0
        alert_message = None
        alert_severity = None
        
        if alerts:
            # Выбрать самый критичный алерт
            critical_alerts = [a for a in alerts if a["severity"] == "critical"]
            warning_alerts = [a for a in alerts if a["severity"] == "warning"]
            
            if critical_alerts:
                alert_severity = "critical"
                alert_message = f"Критические проблемы в {len(critical_alerts)} репозитори{'и' if len(critical_alerts) == 1 else 'ях'}. Требуется внимание!"
            elif warning_alerts:
                alert_severity = "warning"
                alert_message = f"Предупреждения в {len(warning_alerts)} репозитори{'и' if len(warning_alerts) == 1 else 'ях'}. Рекомендуется проверить."
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "repository_count": len(repositories),
            "avg_effectiveness_score": round(avg_effectiveness_score, 2),
            "avg_technical_debt": round(avg_technical_debt, 2),
            "total_active_contributors": total_active_contributors,
            "trend": trend,
            "has_alert": has_alert,
            "alert_message": alert_message,
            "alert_severity": alert_severity,
            "period_start": period_start,
            "period_end": period_end,
        }

    @staticmethod
    def save_project_metric(
        db: Session,
        project_id: int,
        metric_type: str,
        metric_data: Dict,
        score: float,
        trend: str,
        period_start: datetime,
        period_end: datetime,
        has_alert: bool = False,
        alert_message: Optional[str] = None,
        alert_severity: Optional[str] = None
    ):
        """Сохранить метрику проекта в базу данных."""
        metric = ProjectMetric(
            project_id=project_id,
            metric_type=metric_type,
            metric_value=json.dumps(metric_data, default=datetime_converter),
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
        return metric
