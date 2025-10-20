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
                "todo_count": 0,
                "todo_trend": "stable",
                "review_comment_density": 0,
                "technical_debt_score": 50,
                "recommendations": ["No data available for the period"],
                "period_start": period_start,
                "period_end": period_end,
            }
        
        # 1. Test Coverage Analysis
        commits_with_tests = [c for c in commits if c.has_tests]
        test_coverage_delta = sum(c.test_coverage_delta for c in commits if c.test_coverage_delta)
        
        # Simulate current test coverage (in real scenario, get from T1 API)
        base_coverage = 65.0  # Mock base coverage
        current_coverage = max(0, min(100, base_coverage + test_coverage_delta))
        
        if test_coverage_delta > 2:
            coverage_trend = "up"
        elif test_coverage_delta < -2:
            coverage_trend = "down"
        else:
            coverage_trend = "stable"
        
        # 2. TODO Count Analysis
        total_todos = sum(c.todo_count for c in commits)
        avg_todos_per_commit = total_todos / len(commits) if commits else 0
        
        if avg_todos_per_commit > 1:
            todo_trend = "up"
        elif avg_todos_per_commit < 0.5:
            todo_trend = "down"
        else:
            todo_trend = "stable"
        
        # 3. Code Review Comment Density
        if project_id:
            prs = db.query(PullRequest).filter(
                PullRequest.project_id == project_id,
                PullRequest.created_at.between(period_start, period_end)
            ).all()
            
            total_reviews = db.query(CodeReview).filter(
                CodeReview.pull_request_id.in_([pr.id for pr in prs])
            ).all() if prs else []
            
            total_comments = sum(r.comments_count for r in total_reviews)
            review_comment_density = total_comments / len(prs) if prs else 0
        else:
            review_comment_density = 0
        
        # Calculate Technical Debt Score (0-100, lower is worse)
        score_components = []
        
        # Test coverage component (40 points)
        coverage_score = (current_coverage / 100) * 40
        score_components.append(coverage_score)
        
        # TODO trend component (30 points)
        if todo_trend == "down":
            todo_score = 30
        elif todo_trend == "stable":
            todo_score = 20
        else:
            todo_score = max(0, 30 - (avg_todos_per_commit * 5))
        score_components.append(todo_score)
        
        # Review quality component (30 points)
        if review_comment_density > 10:  # Too many comments might indicate poor code quality
            review_score = 15
        elif review_comment_density > 5:
            review_score = 20
        elif review_comment_density > 2:
            review_score = 30
        else:
            review_score = 25  # Too few might mean inadequate review
        score_components.append(review_score)
        
        technical_debt_score = sum(score_components)
        
        # Generate recommendations
        recommendations = []
        
        if current_coverage < 70:
            recommendations.append(
                "Test coverage is below 70%. Increase test coverage to reduce technical debt."
            )
        
        if coverage_trend == "down":
            recommendations.append(
                "⚠️ Test coverage is declining. Ensure new code includes tests."
            )
        
        if todo_trend == "up":
            recommendations.append(
                "TODO comments are increasing. Schedule time to address technical debt."
            )
        
        if review_comment_density > 8:
            recommendations.append(
                "High review comment density suggests code quality issues. Consider pair programming or code reviews earlier in the process."
            )
        
        if not recommendations:
            recommendations.append("Technical debt is under control. Keep up the good work!")
        
        return {
            "team_id": team_id,
            "project_id": project_id,
            "test_coverage": round(current_coverage, 2),
            "test_coverage_trend": coverage_trend,
            "todo_count": total_todos,
            "todo_trend": todo_trend,
            "review_comment_density": round(review_comment_density, 2),
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
