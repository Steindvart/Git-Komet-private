"""
Сервис для анализа технического долга репозитория.
Service for analyzing repository technical debt.
"""
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Repository, Commit, TechnicalDebtMetric
import json


class RepositoryTechnicalDebtService:
    """Сервис для анализа технического долга репозитория на основе TODO комментариев."""

    @staticmethod
    def analyze_technical_debt(
        db: Session,
        repository_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Анализ технического долга репозитория на основе TODO комментариев в коммитах.
        Analyze repository technical debt based on TODO comments in commits.
        """
        repository = db.query(Repository).filter(Repository.id == repository_id).first()
        if not repository:
            return None
        
        # Получить коммиты за период
        commits = db.query(Commit).filter(
            Commit.repository_id == repository_id,
            Commit.committed_at.between(period_start, period_end)
        ).all()
        
        if not commits:
            return {
                "repository_id": repository_id,
                "todo_count": 0,
                "todo_trend": "stable",
                "technical_debt_score": 0.0,
                "recommendations": ["Нет коммитов за указанный период для анализа."],
                "period_start": period_start,
                "period_end": period_end,
            }
        
        # Подсчитать TODO в коде из коммитов
        todo_count = sum(c.todo_count for c in commits)
        
        # Определить тренд TODO
        if todo_count > 50:
            todo_trend = "up"
        elif todo_count < 10:
            todo_trend = "down"
        else:
            todo_trend = "stable"
        
        # Рассчитать оценку технического долга (0-100, меньше лучше)
        technical_debt_score = min(100, (todo_count / 200) * 100)
        
        # Сформировать рекомендации
        recommendations = []
        
        if todo_count == 0:
            recommendations.append("✓ Отлично! Нет TODO комментариев в коммитах.")
        elif todo_count <= 10:
            recommendations.append("✓ Низкий уровень TODO. Продолжайте в том же духе!")
        elif todo_count <= 30:
            recommendations.append("Умеренное количество TODO. Рассмотрите планирование их устранения.")
        elif todo_count <= 50:
            recommendations.append("⚠️ Заметное количество TODO в коде. Создайте задачи для их устранения.")
        elif todo_count <= 100:
            recommendations.append("⚠️ Много TODO в коде. Рекомендуется приоритизировать их устранение.")
        else:
            recommendations.append("🚨 Критическое количество TODO в коде! Необходим план по систематическому устранению технического долга.")
        
        if todo_trend == "up":
            recommendations.append("📈 Количество TODO растет. Необходимо усилить контроль качества кода.")
        elif todo_trend == "down":
            recommendations.append("📉 Количество TODO снижается. Отличная работа по устранению технического долга!")
        
        return {
            "repository_id": repository_id,
            "todo_count": todo_count,
            "todo_trend": todo_trend,
            "technical_debt_score": round(technical_debt_score, 2),
            "recommendations": recommendations,
            "period_start": period_start,
            "period_end": period_end,
        }

    @staticmethod
    def save_technical_debt_metric(
        db: Session,
        repository_id: int,
        metrics: Dict,
        period_start: datetime,
        period_end: datetime
    ):
        """Сохранить метрику технического долга репозитория в базу данных."""
        metric = TechnicalDebtMetric(
            repository_id=repository_id,
            todo_count=metrics["todo_count"],
            todo_trend=metrics["todo_trend"],
            measured_at=datetime.utcnow(),
            period_start=period_start,
            period_end=period_end
        )
        db.add(metric)
        db.commit()
        return metric
