"""
Сервис для анализа технического долга проекта.
Service for analyzing project technical debt.
"""
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Project, TeamMember, Commit, PullRequest, CodeReview, TechnicalDebtMetric
import json


class ProjectTechnicalDebtService:
    """Сервис для анализа технического долга проекта."""

    @staticmethod
    def analyze_technical_debt(
        db: Session,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Анализ технического долга проекта.
        Analyze project technical debt.
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return None
        
        member_ids = [member.id for member in project.members]
        
        # Получить коммиты
        commits = db.query(Commit).filter(
            Commit.author_id.in_(member_ids),
            Commit.committed_at.between(period_start, period_end)
        ).all()
        
        # Получить PR проекта
        prs = db.query(PullRequest).filter(
            PullRequest.project_id == project_id,
            PullRequest.created_at.between(period_start, period_end)
        ).all()
        
        # Рассчитать покрытие тестами
        commits_with_tests = [c for c in commits if c.has_tests]
        test_coverage = (len(commits_with_tests) / len(commits) * 100) if commits else 0
        
        # Определить тренд покрытия тестами (упрощенно)
        test_coverage_trend = "stable"
        if test_coverage > 60:
            test_coverage_trend = "up"
        elif test_coverage < 40:
            test_coverage_trend = "down"
        
        # Подсчитать TODO в коде
        todo_count = sum(c.todo_count for c in commits)
        todo_trend = "stable"
        if todo_count > 50:
            todo_trend = "up"
        
        # Подсчитать TODO в ревью
        pr_ids = [pr.id for pr in prs]
        reviews = db.query(CodeReview).filter(
            CodeReview.pull_request_id.in_(pr_ids)
        ).all()
        
        todo_in_reviews = sum(r.todo_comments for r in reviews)
        
        # Рассчитать плотность комментариев в ревью
        total_review_comments = sum(r.comments_count for r in reviews)
        review_comment_density = (total_review_comments / len(prs)) if prs else 0
        
        # Подсчитать code churn
        churn_commits = [c for c in commits if c.is_churn]
        churn_rate = (len(churn_commits) / len(commits) * 100) if commits else 0
        
        # Рассчитать оценку технического долга (0-100, меньше лучше)
        debt_components = []
        
        # 1. Покрытие тестами (0-30 баллов долга)
        test_debt = max(0, 30 - (test_coverage / 100 * 30))
        debt_components.append(test_debt)
        
        # 2. TODO в коде (0-20 баллов долга)
        todo_debt = min(20, (todo_count / 100) * 20)
        debt_components.append(todo_debt)
        
        # 3. TODO в ревью (0-15 баллов долга)
        review_todo_debt = min(15, (todo_in_reviews / 50) * 15)
        debt_components.append(review_todo_debt)
        
        # 4. Code churn (0-20 баллов долга)
        churn_debt = min(20, (churn_rate / 100) * 20)
        debt_components.append(churn_debt)
        
        # 5. Качество ревью (0-15 баллов долга)
        # Слишком мало комментариев = плохо, слишком много = тоже плохо
        if review_comment_density < 2:
            review_quality_debt = 15
        elif review_comment_density > 10:
            review_quality_debt = 10
        else:
            review_quality_debt = 5
        debt_components.append(review_quality_debt)
        
        technical_debt_score = sum(debt_components)
        
        # Сформировать рекомендации
        recommendations = []
        
        if test_coverage < 50:
            recommendations.append("⚠️ Низкое покрытие тестами. Рекомендуется увеличить до 60%+.")
        elif test_coverage < 70:
            recommendations.append("Покрытие тестами можно улучшить. Стремитесь к 70%+.")
        else:
            recommendations.append("✓ Хорошее покрытие тестами. Продолжайте поддерживать уровень!")
        
        if todo_count > 100:
            recommendations.append("⚠️ Очень много TODO в коде. Создайте задачи для их устранения.")
        elif todo_count > 50:
            recommendations.append("Много TODO в коде. Рассмотрите планирование их устранения.")
        
        if todo_in_reviews > 30:
            recommendations.append("⚠️ Много TODO в ревью. Оформляйте их как отдельные задачи.")
        elif todo_in_reviews > 15:
            recommendations.append("TODO в ревью растут. Следите за этим показателем.")
        
        if churn_rate > 30:
            recommendations.append("⚠️ Высокий code churn. Проверьте качество планирования и дизайна.")
        elif churn_rate > 20:
            recommendations.append("Умеренный code churn. Можно улучшить планирование.")
        
        if review_comment_density < 2:
            recommendations.append("Мало комментариев в ревью. Возможно, ревью недостаточно тщательные.")
        elif review_comment_density > 10:
            recommendations.append("Много комментариев в ревью. Возможно, стоит улучшить качество кода до ревью.")
        
        return {
            "project_id": project_id,
            "test_coverage": round(test_coverage, 2),
            "test_coverage_trend": test_coverage_trend,
            "todo_count": todo_count,
            "todo_in_reviews": todo_in_reviews,
            "todo_trend": todo_trend,
            "churn_rate": round(churn_rate, 2),
            "review_comment_density": round(review_comment_density, 2),
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
            test_coverage=metrics.get("test_coverage"),
            test_coverage_trend=metrics.get("test_coverage_trend"),
            todo_count=metrics.get("todo_count", 0),
            todo_trend=metrics.get("todo_trend"),
            review_comment_density=metrics.get("review_comment_density"),
            measured_at=datetime.utcnow(),
            period_start=period_start,
            period_end=period_end
        )
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return metric
