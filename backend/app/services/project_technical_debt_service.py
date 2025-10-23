"""
Сервис для анализа технического долга проекта.
Service for analyzing project technical debt.

Новое ТЗ: Доступны только git коммиты и их diff.
Технический долг теперь анализируется ТОЛЬКО по TODO комментариям из diff коммитов.
"""
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Project, ProjectMember, Commit, TechnicalDebtMetric
import json


class ProjectTechnicalDebtService:
    """Сервис для анализа технического долга проекта на основе TODO комментариев."""

    @staticmethod
    def analyze_technical_debt(
        db: Session,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Анализ технического долга проекта на основе TODO комментариев в коммитах.
        Analyze project technical debt based on TODO comments in commits.
        
        Новое ТЗ: Фокус ТОЛЬКО на TODO комментариях из diff коммитов.
        Убрали: покрытие тестами, метрики ревью, code churn.
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return None
        
        member_ids = [member.id for member in project.members]
        
        # Получить коммиты за период
        commits = db.query(Commit).filter(
            Commit.author_id.in_(member_ids),
            Commit.committed_at.between(period_start, period_end)
        ).all()
        
        if not commits:
            return {
                "project_id": project_id,
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
        # Упрощенная логика: сравниваем с пороговыми значениями
        if todo_count > 50:
            todo_trend = "up"  # Растет
        elif todo_count < 10:
            todo_trend = "down"  # Снижается
        else:
            todo_trend = "stable"  # Стабильно
        
        # Рассчитать оценку технического долга (0-100, меньше лучше)
        # Оценка основана ТОЛЬКО на количестве TODO
        # 0 TODO = 0 баллов долга (отлично)
        # 100 TODO = 50 баллов долга
        # 200+ TODO = 100 баллов долга (критично)
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
        
        # Добавить рекомендацию по тренду
        if todo_trend == "up":
            recommendations.append("📈 Количество TODO растет. Необходимо усилить контроль качества кода.")
        elif todo_trend == "down":
            recommendations.append("📉 Количество TODO снижается. Отличная работа по устранению технического долга!")
        
        return {
            "project_id": project_id,
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
        project_id: int,
        metrics: Dict,
        period_start: datetime,
        period_end: datetime
    ) -> TechnicalDebtMetric:
        """Сохранить метрику технического долга в базу данных."""
        metric = TechnicalDebtMetric(
            project_id=project_id,
            test_coverage=None,  # Больше не используется в новом ТЗ
            test_coverage_trend=None,  # Больше не используется в новом ТЗ
            todo_count=metrics.get("todo_count", 0),
            todo_trend=metrics.get("todo_trend"),
            review_comment_density=None,  # Больше не используется в новом ТЗ
            measured_at=datetime.utcnow(),
            period_start=period_start,
            period_end=period_end
        )
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return metric
