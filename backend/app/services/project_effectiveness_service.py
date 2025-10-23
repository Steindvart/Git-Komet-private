"""
Сервис для расчёта метрик эффективности проекта.
Service for calculating project effectiveness metrics.

Новое ТЗ: Доступны только git коммиты, ветки, репозитории и diff коммитов.
Добавлены новые метрики:
- Активные участники (уникальные авторы коммитов за период)
- Количество коммитов на человека (для оценки экспертности)
"""
from typing import Dict, Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Project, ProjectMember, Commit, ProjectMetric
import json


class ProjectEffectivenessService:
    """Сервис для расчёта общей оценки эффективности проекта."""

    @staticmethod
    def calculate_active_contributors(
        db: Session,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Рассчитать метрику активных участников проекта.
        Calculate active contributors metric for the project.
        
        Новое ТЗ: Берем все коммиты за последний месяц и считаем уникальных авторов.
        Каждый уникальный автор - это активный участник.
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return None
        
        member_ids = [member.id for member in project.members]
        
        # Получить все коммиты за период
        commits = db.query(Commit).filter(
            Commit.author_id.in_(member_ids),
            Commit.committed_at.between(period_start, period_end)
        ).all()
        
        if not commits:
            return {
                "project_id": project_id,
                "project_name": project.name,
                "active_contributors": 0,
                "total_commits": 0,
                "period_start": period_start,
                "period_end": period_end,
            }
        
        # Подсчитать уникальных авторов
        unique_authors = set()
        for commit in commits:
            if commit.author_id:
                unique_authors.add(commit.author_id)
        
        active_contributors = len(unique_authors)
        total_commits = len(commits)
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "active_contributors": active_contributors,
            "total_commits": total_commits,
            "avg_commits_per_contributor": round(total_commits / active_contributors, 2) if active_contributors > 0 else 0,
            "period_start": period_start,
            "period_end": period_end,
        }

    @staticmethod
    def calculate_commits_per_person(
        db: Session,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Рассчитать количество коммитов на каждого участника для оценки экспертности.
        Calculate commit count per person to understand expertise level.
        
        Новое ТЗ: Количество коммитов на того или иного человека,
        чтобы понимать уровень экспертности по проекту.
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return None
        
        member_ids = [member.id for member in project.members]
        
        # Получить все коммиты за период, сгруппированные по автору
        commit_counts = db.query(
            Commit.author_id,
            func.count(Commit.id).label('commit_count'),
            func.sum(Commit.insertions + Commit.deletions).label('lines_changed')
        ).filter(
            Commit.author_id.in_(member_ids),
            Commit.committed_at.between(period_start, period_end)
        ).group_by(Commit.author_id).all()
        
        # Получить информацию об участниках
        members = db.query(ProjectMember).filter(ProjectMember.id.in_(member_ids)).all()
        member_map = {m.id: m for m in members}
        
        # Сформировать список участников с метриками
        contributors = []
        for author_id, commit_count, lines_changed in commit_counts:
            member = member_map.get(author_id)
            if member:
                # Определить уровень экспертности на основе количества коммитов
                if commit_count >= 50:
                    expertise_level = "expert"
                elif commit_count >= 20:
                    expertise_level = "advanced"
                elif commit_count >= 5:
                    expertise_level = "intermediate"
                else:
                    expertise_level = "beginner"
                
                contributors.append({
                    "author_id": author_id,
                    "author_name": member.name,
                    "author_email": member.email,
                    "commit_count": commit_count,
                    "lines_changed": int(lines_changed) if lines_changed else 0,
                    "expertise_level": expertise_level
                })
        
        # Сортировать по количеству коммитов (убывание)
        contributors.sort(key=lambda x: x["commit_count"], reverse=True)
        
        return {
            "project_id": project_id,
            "project_name": project.name,
            "contributors": contributors,
            "total_contributors": len(contributors),
            "period_start": period_start,
            "period_end": period_end,
        }

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
        
        Новое ТЗ: Оценка основана только на данных коммитов (без PR и задач).
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
        
        if not commits:
            return {
                "project_id": project_id,
                "project_name": project.name,
                "effectiveness_score": 0.0,
                "trend": "stable",
                "total_commits": 0,
                "active_contributors": 0,
                "after_hours_percentage": 0.0,
                "weekend_percentage": 0.0,
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
        
        # Рассчитать оценку эффективности (0-100)
        # Чем выше, тем лучше
        score_components = []
        
        # 1. Активность коммитов (макс 30 баллов)
        commit_score = min(30, (total_commits / max(len(member_ids), 1)) * 6) if member_ids else 0
        score_components.append(commit_score)
        
        # 2. Вовлеченность команды (макс 30 баллов)
        collab_score = (active_contributors / max(len(member_ids), 1)) * 30 if member_ids else 0
        score_components.append(collab_score)
        
        # 3. Work-life balance (макс 20 баллов) - штраф за переработки
        if after_hours_percentage > 30 or weekend_percentage > 20:
            work_life_score = max(0, 20 - (after_hours_percentage / 10))
        else:
            work_life_score = 20
        score_components.append(work_life_score)
        
        # 4. Качество кода (макс 20 баллов) - штраф за высокий churn
        if churn_rate > 25:
            quality_score = max(0, 20 - (churn_rate / 10))
        else:
            quality_score = 20
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
            alert_message = "Эффективность проекта ниже целевого уровня. Проверьте активность команды."
            alert_severity = "critical"
        elif effectiveness_score < 60:
            has_alert = True
            alert_message = "Эффективность проекта может быть улучшена. Рассмотрите оптимизацию процессов."
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
