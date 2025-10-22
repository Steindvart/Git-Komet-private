"""
Сервис для расчёта метрик эффективности проекта.
Service for calculating project effectiveness metrics.
"""
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Project, TeamMember, Commit, PullRequest, Task, ProjectMetric
import json


class ProjectEffectivenessService:
    """Сервис для расчёта общей оценки эффективности проекта."""

    @staticmethod
    def calculate_effectiveness_score(
        db: Session,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Рассчитать комплексную оценку эффективности проекта.
        Calculate comprehensive project effectiveness score.
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return None
        
        # Получить участников проекта
        member_ids = [member.id for member in project.members]
        
        # Получить коммиты участников проекта
        commits = db.query(Commit).filter(
            Commit.author_id.in_(member_ids),
            Commit.committed_at.between(period_start, period_end)
        ).all()
        
        # Получить PR проекта
        prs = db.query(PullRequest).filter(
            PullRequest.project_id == project_id,
            PullRequest.created_at.between(period_start, period_end)
        ).all()
        
        # Получить задачи проекта
        tasks = db.query(Task).filter(
            Task.project_id == project_id,
            Task.created_at.between(period_start, period_end)
        ).all()
        
        # Рассчитать метрики
        total_commits = len(commits)
        total_prs = len(prs)
        active_contributors = len(set(c.author_id for c in commits if c.author_id))
        
        # Среднее время первого ревью для PR
        pr_review_times = [pr.time_to_first_review for pr in prs if pr.time_to_first_review]
        avg_pr_review_time = sum(pr_review_times) / len(pr_review_times) if pr_review_times else 0
        
        # Метрики work-life balance
        after_hours_commits = [c for c in commits if c.is_after_hours]
        weekend_commits = [c for c in commits if c.is_weekend]
        after_hours_percentage = (len(after_hours_commits) / total_commits * 100) if total_commits > 0 else 0
        weekend_percentage = (len(weekend_commits) / total_commits * 100) if total_commits > 0 else 0
        
        # Метрики code churn
        churn_commits = [c for c in commits if c.is_churn]
        churn_rate = (len(churn_commits) / total_commits * 100) if total_commits > 0 else 0
        
        # Рассчитать оценку эффективности (0-100)
        # Чем выше, тем лучше
        score_components = []
        
        # 1. Активность коммитов (макс 20 баллов)
        commit_score = min(20, (total_commits / max(len(member_ids), 1)) * 4) if member_ids else 0
        score_components.append(commit_score)
        
        # 2. Производительность PR (макс 20 баллов)
        pr_score = min(20, (total_prs / max(len(member_ids), 1)) * 8) if member_ids else 0
        score_components.append(pr_score)
        
        # 3. Эффективность ревью (макс 20 баллов) - быстрее лучше
        if avg_pr_review_time > 0:
            review_score = max(0, 20 - (avg_pr_review_time / 24) * 4)
        else:
            review_score = 12
        score_components.append(review_score)
        
        # 4. Вовлеченность команды (макс 20 баллов)
        collab_score = (active_contributors / max(len(member_ids), 1)) * 20 if member_ids else 0
        score_components.append(collab_score)
        
        # 5. Work-life balance (макс 10 баллов) - штраф за переработки
        if after_hours_percentage > 30 or weekend_percentage > 20:
            work_life_score = max(0, 10 - (after_hours_percentage / 10))
        else:
            work_life_score = 10
        score_components.append(work_life_score)
        
        # 6. Качество кода (макс 10 баллов) - штраф за высокий churn
        if churn_rate > 25:
            quality_score = max(0, 10 - (churn_rate / 10))
        else:
            quality_score = 10
        score_components.append(quality_score)
        
        effectiveness_score = sum(score_components)
        
        # Определить тренд (упрощенно - сравнить с предыдущим периодом)
        trend = "stable"
        
        # Проверить на алерты
        has_alert = False
        alert_message = None
        alert_severity = None
        
        if effectiveness_score < 40:
            has_alert = True
            alert_message = "Эффективность проекта ниже целевого уровня. Проверьте узкие места и загруженность команды."
            alert_severity = "critical"
        elif effectiveness_score < 60:
            has_alert = True
            alert_message = "Эффективность проекта может быть улучшена. Рассмотрите оптимизацию процессов."
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
            "project_id": project_id,
            "project_name": project.name,
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
            "period_start": period_start,
            "period_end": period_end,
        }

    @staticmethod
    def calculate_employee_care_metric(
        db: Session,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Рассчитать агрегированную метрику "забота о сотрудниках" для проекта.
        Calculate aggregated employee care metric for the project.
        
        Эта метрика отслеживает work-life balance на уровне проекта.
        This metric tracks work-life balance at the project level.
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return None
        
        member_ids = [member.id for member in project.members]
        
        # Получить все коммиты участников
        commits = db.query(Commit).filter(
            Commit.author_id.in_(member_ids),
            Commit.committed_at.between(period_start, period_end)
        ).all()
        
        if not commits:
            return {
                "project_id": project_id,
                "project_name": project.name,
                "employee_care_score": 100.0,
                "after_hours_percentage": 0.0,
                "weekend_percentage": 0.0,
                "status": "excellent",
                "recommendations": [],
                "period_start": period_start,
                "period_end": period_end,
            }
        
        total_commits = len(commits)
        after_hours_commits = [c for c in commits if c.is_after_hours]
        weekend_commits = [c for c in commits if c.is_weekend]
        
        after_hours_percentage = (len(after_hours_commits) / total_commits * 100)
        weekend_percentage = (len(weekend_commits) / total_commits * 100)
        
        # Рассчитать оценку заботы о сотрудниках (0-100)
        # 100 - отлично (нет переработок), 0 - критично (постоянные переработки)
        care_score = 100.0
        
        # Штрафы за активность после рабочего времени
        if after_hours_percentage > 10:
            care_score -= (after_hours_percentage - 10) * 1.5
        
        # Штрафы за активность в выходные
        if weekend_percentage > 5:
            care_score -= (weekend_percentage - 5) * 2.0
        
        care_score = max(0.0, care_score)
        
        # Определить статус
        if care_score >= 80:
            status = "excellent"
        elif care_score >= 60:
            status = "good"
        elif care_score >= 40:
            status = "needs_attention"
        else:
            status = "critical"
        
        # Сформировать рекомендации
        recommendations = []
        if after_hours_percentage > 30:
            recommendations.append("Критический уровень активности после рабочего времени. Необходимо пересмотреть планирование и нагрузку на команду.")
        elif after_hours_percentage > 20:
            recommendations.append("Высокий уровень активности после рабочего времени. Рекомендуется проверить распределение задач.")
        elif after_hours_percentage > 10:
            recommendations.append("Умеренная активность после рабочего времени. Следите за балансом работы и отдыха.")
        
        if weekend_percentage > 20:
            recommendations.append("Критический уровень работы в выходные. Необходимо срочно пересмотреть процессы.")
        elif weekend_percentage > 10:
            recommendations.append("Высокая активность в выходные дни. Рассмотрите перераспределение нагрузки.")
        elif weekend_percentage > 5:
            recommendations.append("Есть работа в выходные. Убедитесь, что это не систематическая проблема.")
        
        if not recommendations:
            recommendations.append("Отличный баланс работы и жизни! Продолжайте поддерживать здоровую рабочую культуру.")
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "employee_care_score": round(care_score, 2),
            "after_hours_percentage": round(after_hours_percentage, 2),
            "weekend_percentage": round(weekend_percentage, 2),
            "status": status,
            "recommendations": recommendations,
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
        alert_message: str = None,
        alert_severity: str = None
    ) -> ProjectMetric:
        """Сохранить метрику проекта в базу данных."""
        metric = ProjectMetric(
            project_id=project_id,
            metric_type=metric_type,
            metric_value=json.dumps(metric_data, default=str),
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
