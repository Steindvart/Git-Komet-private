"""
Сервис для расчёта метрик эффективности репозитория.
Service for calculating repository effectiveness metrics.
"""
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Repository, ProjectMember, Commit, RepositoryMetric
import json


class RepositoryEffectivenessService:
    """Сервис для расчёта общей оценки эффективности репозитория."""

    @staticmethod
    def calculate_effectiveness_score(
        db: Session,
        repository_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Рассчитать комплексную оценку эффективности репозитория.
        Calculate comprehensive repository effectiveness score.
        """
        repository = db.query(Repository).filter(Repository.id == repository_id).first()
        if not repository:
            return None
        
        # Получить коммиты репозитория
        commits = db.query(Commit).filter(
            Commit.repository_id == repository_id,
            Commit.committed_at.between(period_start, period_end)
        ).all()
        
        if not commits:
            return {
                "repository_id": repository_id,
                "repository_name": repository.name,
                "effectiveness_score": 0.0,
                "trend": "stable",
                "total_commits": 0,
                "active_contributors": 0,
                "after_hours_percentage": 0.0,
                "weekend_percentage": 0.0,
                "churn_rate": 0.0,
                "has_alert": False,
                "alert_message": None,
                "alert_severity": None,
                "period_start": period_start,
                "period_end": period_end,
            }
        
        # Рассчитать метрики
        total_commits = len(commits)
        active_contributors = len(set(c.author_id for c in commits if c.author_id))
        
        # Метрики work-life balance
        after_hours_commits = [c for c in commits if c.is_after_hours]
        weekend_commits = [c for c in commits if c.is_weekend]
        after_hours_percentage = (len(after_hours_commits) / total_commits * 100) if total_commits > 0 else 0
        weekend_percentage = (len(weekend_commits) / total_commits * 100) if total_commits > 0 else 0
        
        # Метрики code churn
        churn_commits = [c for c in commits if c.is_churn]
        churn_rate = (len(churn_commits) / total_commits * 100) if total_commits > 0 else 0
        
        # Рассчитать общую оценку эффективности
        score = 100.0
        
        # Штрафы за work-life balance
        if after_hours_percentage > 30:
            score -= min(20, (after_hours_percentage - 30) * 0.5)
        
        if weekend_percentage > 20:
            score -= min(20, (weekend_percentage - 20) * 0.7)
        
        # Штрафы за code churn
        if churn_rate > 15:
            score -= min(15, (churn_rate - 15) * 0.5)
        
        # Бонусы за активность
        if total_commits >= 50:
            score += min(10, total_commits / 10)
        
        if active_contributors >= 3:
            score += min(10, active_contributors * 2)
        
        score = max(0, min(100, round(score, 2)))
        
        # Определить тренд (в упрощенном варианте - stable)
        trend = "stable"
        if score >= 80:
            trend = "improving"
        elif score < 50:
            trend = "declining"
        
        # Проверить на алерты
        has_alert = False
        alert_message = None
        alert_severity = None
        
        if after_hours_percentage > 40:
            has_alert = True
            alert_message = f"Обнаружена высокая активность вне рабочего времени ({after_hours_percentage:.1f}%)"
            alert_severity = "warning"
        
        if weekend_percentage > 30:
            has_alert = True
            alert_message = f"Обнаружена высокая активность в выходные дни ({weekend_percentage:.1f}%)"
            alert_severity = "critical"
        
        return {
            "repository_id": repository_id,
            "repository_name": repository.name,
            "effectiveness_score": score,
            "trend": trend,
            "total_commits": total_commits,
            "active_contributors": active_contributors,
            "after_hours_percentage": round(after_hours_percentage, 2),
            "weekend_percentage": round(weekend_percentage, 2),
            "churn_rate": round(churn_rate, 2),
            "has_alert": has_alert,
            "alert_message": alert_message,
            "alert_severity": alert_severity,
            "period_start": period_start,
            "period_end": period_end,
        }

    @staticmethod
    def calculate_employee_care_metric(
        db: Session,
        repository_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Рассчитать агрегированную метрику заботы о сотрудниках для репозитория.
        Calculate aggregated employee care metric for repository.
        """
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
                "employee_care_score": 100.0,
                "after_hours_percentage": 0.0,
                "weekend_percentage": 0.0,
                "status": "excellent",
                "recommendations": [],
                "period_start": period_start,
                "period_end": period_end,
            }
        
        total_commits = len(commits)
        after_hours_commits = len([c for c in commits if c.is_after_hours])
        weekend_commits = len([c for c in commits if c.is_weekend])
        
        after_hours_percentage = (after_hours_commits / total_commits * 100) if total_commits > 0 else 0
        weekend_percentage = (weekend_commits / total_commits * 100) if total_commits > 0 else 0
        
        # Рассчитать оценку
        score = 100.0
        
        # Штрафы
        if after_hours_percentage > 10:
            score -= (after_hours_percentage - 10) * 1.5
        
        if weekend_percentage > 5:
            score -= (weekend_percentage - 5) * 2.0
        
        score = max(0, min(100, round(score, 2)))
        
        # Определить статус
        if score >= 80:
            status = "excellent"
        elif score >= 60:
            status = "good"
        elif score >= 40:
            status = "needs_attention"
        else:
            status = "critical"
        
        # Рекомендации
        recommendations = []
        if after_hours_percentage > 30:
            recommendations.append(f"Критический уровень активности после рабочего времени ({after_hours_percentage:.1f}%). Рекомендуется пересмотреть нагрузку команды.")
        elif after_hours_percentage > 15:
            recommendations.append(f"Повышенная активность после рабочего времени ({after_hours_percentage:.1f}%). Следует обратить внимание на work-life balance.")
        
        if weekend_percentage > 20:
            recommendations.append(f"Критический уровень работы в выходные ({weekend_percentage:.1f}%). Необходимо обеспечить отдых команды.")
        elif weekend_percentage > 10:
            recommendations.append(f"Повышенная активность в выходные ({weekend_percentage:.1f}%). Рекомендуется оптимизировать планирование.")
        
        if not recommendations and score < 100:
            recommendations.append("Хороший баланс, но есть возможности для улучшения.")
        elif not recommendations:
            recommendations.append("Отличный баланс работы и отдыха!")
        
        return {
            "repository_id": repository_id,
            "repository_name": repository.name,
            "employee_care_score": score,
            "after_hours_percentage": round(after_hours_percentage, 2),
            "weekend_percentage": round(weekend_percentage, 2),
            "status": status,
            "recommendations": recommendations,
            "period_start": period_start,
            "period_end": period_end,
        }

    @staticmethod
    def save_repository_metric(
        db: Session,
        repository_id: int,
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
        """Сохранить метрику репозитория в базу данных."""
        metric = RepositoryMetric(
            repository_id=repository_id,
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
        return metric
