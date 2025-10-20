from typing import Dict, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Team, TeamMember, Commit, CodeReview, PullRequest, TechnicalDebtMetric
import json


class TechnicalDebtService:
    """Service for analyzing technical debt trends."""

    @staticmethod
    def analyze_technical_debt(
        db: Session,
        team_id: int = None,
        project_id: int = None,
        period_start: datetime = None,
        period_end: datetime = None
    ) -> Dict:
        """Analyze technical debt metrics."""
        
        # Get commits in period
        query = db.query(Commit).filter(
            Commit.committed_at.between(period_start, period_end)
        )
        
        if team_id:
            team = db.query(Team).filter(Team.id == team_id).first()
            if team:
                member_ids = [m.id for m in team.members]
                query = query.filter(Commit.author_id.in_(member_ids))
        
        commits = query.all()
        
        if not commits:
            return {
                "team_id": team_id,
                "project_id": project_id,
                "test_coverage": 0,
                "test_coverage_trend": "stable",
                "todo_count_code": 0,
                "todo_count_reviews": 0,
                "todo_trend": "stable",
                "review_comment_density": 0,
                "churn_rate": 0,
                "technical_debt_score": 50,
                "recommendations": ["Нет данных за указанный период"],
                "period_start": period_start,
                "period_end": period_end,
            }
        
        # 1. Test Coverage Analysis
        commits_with_tests = [c for c in commits if c.has_tests]
        test_coverage_delta = sum(c.test_coverage_delta for c in commits if c.test_coverage_delta)
        
        # Simulate current test coverage (in real scenario, get from Git API or code analysis)
        base_coverage = 65.0  # Mock base coverage
        current_coverage = max(0, min(100, base_coverage + test_coverage_delta))
        
        if test_coverage_delta > 2:
            coverage_trend = "up"
        elif test_coverage_delta < -2:
            coverage_trend = "down"
        else:
            coverage_trend = "stable"
        
        # 2. TODO Count Analysis - from code commits
        total_todos_code = sum(c.todo_count for c in commits)
        avg_todos_per_commit = total_todos_code / len(commits) if commits else 0
        
        # Get TODO comments from reviews
        total_todos_reviews = 0
        if project_id:
            prs = db.query(PullRequest).filter(
                PullRequest.project_id == project_id,
                PullRequest.created_at.between(period_start, period_end)
            ).all()
            
            total_reviews = db.query(CodeReview).filter(
                CodeReview.pull_request_id.in_([pr.id for pr in prs])
            ).all() if prs else []
            
            total_todos_reviews = sum(r.todo_comments for r in total_reviews)
            total_comments = sum(r.comments_count for r in total_reviews)
            review_comment_density = total_comments / len(prs) if prs else 0
        else:
            review_comment_density = 0
        
        # Determine TODO trend
        if avg_todos_per_commit > 1.5 or total_todos_reviews > 10:
            todo_trend = "up"
        elif avg_todos_per_commit < 0.3 and total_todos_reviews < 5:
            todo_trend = "down"
        else:
            todo_trend = "stable"
        
        # 3. Code Churn Analysis
        churn_commits = [c for c in commits if c.is_churn]
        churn_rate = (len(churn_commits) / len(commits) * 100) if commits else 0
        
        # Calculate Technical Debt Score (0-100, higher is better)
        score_components = []
        
        # Test coverage component (30 points)
        coverage_score = (current_coverage / 100) * 30
        score_components.append(coverage_score)
        
        # TODO trend component (25 points)
        if todo_trend == "down":
            todo_score = 25
        elif todo_trend == "stable":
            todo_score = 15
        else:
            todo_score = max(0, 25 - (avg_todos_per_commit * 5))
        score_components.append(todo_score)
        
        # Review quality component (25 points)
        if review_comment_density > 10:  # Too many comments might indicate poor code quality
            review_score = 12
        elif review_comment_density > 5:
            review_score = 18
        elif review_comment_density > 2:
            review_score = 25
        else:
            review_score = 20  # Too few might mean inadequate review
        score_components.append(review_score)
        
        # Code churn component (20 points)
        if churn_rate < 15:
            churn_score = 20
        elif churn_rate < 25:
            churn_score = 15
        else:
            churn_score = max(0, 20 - (churn_rate / 5))
        score_components.append(churn_score)
        
        technical_debt_score = sum(score_components)
        
        # Generate recommendations in Russian
        recommendations = []
        
        if current_coverage < 70:
            recommendations.append(
                "Покрытие тестами ниже 70%. Увеличьте покрытие тестами для снижения технического долга."
            )
        
        if coverage_trend == "down":
            recommendations.append(
                "⚠️ Покрытие тестами снижается. Убедитесь, что новый код включает тесты."
            )
        
        if todo_trend == "up":
            recommendations.append(
                f"TODO комментарии растут (в коде: {total_todos_code}, в ревью: {total_todos_reviews}). "
                "Запланируйте время для работы с техническим долгом."
            )
        
        if total_todos_reviews > 15:
            recommendations.append(
                "Высокое количество TODO предложений в ревью. Рассмотрите возможность оформления их в отдельные тикеты."
            )
        
        if review_comment_density > 8:
            recommendations.append(
                "Высокая плотность комментариев в ревью указывает на проблемы с качеством кода. "
                "Рассмотрите парное программирование или более раннее ревью кода."
            )
        
        if churn_rate > 25:
            recommendations.append(
                f"⚠️ Высокий уровень переписывания кода ({churn_rate:.1f}%). "
                "Это может указывать на проблемы с планированием или качеством исходного кода."
            )
        
        if not recommendations:
            recommendations.append("Технический долг под контролем. Продолжайте в том же духе!")
        
        return {
            "team_id": team_id,
            "project_id": project_id,
            "test_coverage": round(current_coverage, 2),
            "test_coverage_trend": coverage_trend,
            "todo_count_code": total_todos_code,
            "todo_count_reviews": total_todos_reviews,
            "todo_trend": todo_trend,
            "review_comment_density": round(review_comment_density, 2),
            "churn_rate": round(churn_rate, 2),
            "technical_debt_score": round(technical_debt_score, 2),
            "recommendations": recommendations,
            "period_start": period_start,
            "period_end": period_end,
        }

    @staticmethod
    def save_technical_debt_metric(
        db: Session,
        team_id: int = None,
        project_id: int = None,
        metrics: Dict = None,
        period_start: datetime = None,
        period_end: datetime = None
    ) -> TechnicalDebtMetric:
        """Save technical debt metric to database."""
        metric = TechnicalDebtMetric(
            team_id=team_id,
            project_id=project_id,
            test_coverage=metrics.get("test_coverage"),
            test_coverage_trend=metrics.get("test_coverage_trend"),
            todo_count=metrics.get("todo_count"),
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
