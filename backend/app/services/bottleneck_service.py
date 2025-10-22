from sqlalchemy.orm import Session
from app.models.database_models import Project, PullRequest, Issue, Metric
from app.models.schemas import BottleneckAnalysis
from datetime import datetime, timedelta
from typing import Optional


class BottleneckService:
    """Сервис для анализа узких мест в проекте"""

    @staticmethod
    def calculate_time_delta_hours(start: Optional[datetime], end: Optional[datetime]) -> Optional[float]:
        """Вычисление разницы во времени в часах"""
        if not start or not end:
            return None
        delta = end - start
        return delta.total_seconds() / 3600

    @staticmethod
    def analyze_project(db: Session, project_id: int) -> BottleneckAnalysis:
        """Анализ узких мест проекта"""
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise ValueError(f"Project with id {project_id} not found")

        # Получаем все PR проекта
        pull_requests = db.query(PullRequest).filter(PullRequest.project_id == project_id).all()
        
        # Анализ времени на PR
        pr_review_times = []
        pr_approval_times = []
        pr_merge_times = []
        
        for pr in pull_requests:
            # Время до первого ревью
            review_time = BottleneckService.calculate_time_delta_hours(pr.created_at, pr.first_review_at)
            if review_time:
                pr_review_times.append(review_time)
            
            # Время до одобрения
            approval_time = BottleneckService.calculate_time_delta_hours(pr.created_at, pr.approved_at)
            if approval_time:
                pr_approval_times.append(approval_time)
            
            # Время до мерджа
            merge_time = BottleneckService.calculate_time_delta_hours(pr.created_at, pr.merged_at)
            if merge_time:
                pr_merge_times.append(merge_time)

        # Получаем все задачи проекта
        issues = db.query(Issue).filter(Issue.project_id == project_id).all()
        
        # Анализ времени на задачи
        issue_start_times = []
        issue_completion_times = []
        
        for issue in issues:
            # Время до начала работы
            start_time = BottleneckService.calculate_time_delta_hours(issue.created_at, issue.started_at)
            if start_time:
                issue_start_times.append(start_time)
            
            # Время выполнения
            completion_time = BottleneckService.calculate_time_delta_hours(issue.started_at, issue.completed_at)
            if completion_time:
                issue_completion_times.append(completion_time)

        # Вычисление средних значений
        avg_pr_review_time = sum(pr_review_times) / len(pr_review_times) if pr_review_times else None
        avg_pr_approval_time = sum(pr_approval_times) / len(pr_approval_times) if pr_approval_times else None
        avg_pr_merge_time = sum(pr_merge_times) / len(pr_merge_times) if pr_merge_times else None
        avg_issue_start_time = sum(issue_start_times) / len(issue_start_times) if issue_start_times else None
        avg_issue_completion_time = sum(issue_completion_times) / len(issue_completion_times) if issue_completion_times else None

        # Определение узких мест и рекомендаций
        bottlenecks = []
        recommendations = []

        # Порог для PR ревью - 24 часа
        if avg_pr_review_time and avg_pr_review_time > 24:
            bottlenecks.append(f"Долгое ожидание первого ревью PR (среднее: {avg_pr_review_time:.1f} часов)")
            recommendations.append("Рекомендация: Установить SLA на первое ревью в пределах 4-8 часов")

        # Порог для одобрения PR - 48 часов
        if avg_pr_approval_time and avg_pr_approval_time > 48:
            bottlenecks.append(f"Долгое одобрение PR (среднее: {avg_pr_approval_time:.1f} часов)")
            recommendations.append("Рекомендация: Автоматизировать процесс ревью, назначать ответственных ревьюеров")

        # Порог для мерджа PR - 72 часа
        if avg_pr_merge_time and avg_pr_merge_time > 72:
            bottlenecks.append(f"Долгий процесс мерджа PR (среднее: {avg_pr_merge_time:.1f} часов)")
            recommendations.append("Рекомендация: Оптимизировать процесс CI/CD, уменьшить размер PR")

        # Порог для начала работы над задачей - 48 часов
        if avg_issue_start_time and avg_issue_start_time > 48:
            bottlenecks.append(f"Задачи долго не берутся в работу (среднее: {avg_issue_start_time:.1f} часов)")
            recommendations.append("Рекомендация: Улучшить приоритизацию задач, провести планирование")

        # Порог для выполнения задачи - 168 часов (неделя)
        if avg_issue_completion_time and avg_issue_completion_time > 168:
            bottlenecks.append(f"Задачи долго выполняются (среднее: {avg_issue_completion_time:.1f} часов)")
            recommendations.append("Рекомендация: Декомпозировать задачи на более мелкие, устранить блокеры")

        if not bottlenecks:
            recommendations.append("Процесс работы в проекте выглядит эффективным, узких мест не обнаружено")

        # Сохранение метрик в БД
        BottleneckService.save_metrics(
            db, project_id, 
            avg_pr_review_time, avg_pr_approval_time, avg_pr_merge_time,
            avg_issue_start_time, avg_issue_completion_time
        )

        return BottleneckAnalysis(
            project_id=project_id,
            project_name=project.name,
            avg_pr_review_time_hours=avg_pr_review_time,
            avg_pr_approval_time_hours=avg_pr_approval_time,
            avg_pr_merge_time_hours=avg_pr_merge_time,
            avg_issue_start_time_hours=avg_issue_start_time,
            avg_issue_completion_time_hours=avg_issue_completion_time,
            total_prs=len(pull_requests),
            total_issues=len(issues),
            bottlenecks=bottlenecks,
            recommendations=recommendations
        )

    @staticmethod
    def save_metrics(
        db: Session, 
        project_id: int,
        avg_pr_review_time: Optional[float],
        avg_pr_approval_time: Optional[float],
        avg_pr_merge_time: Optional[float],
        avg_issue_start_time: Optional[float],
        avg_issue_completion_time: Optional[float]
    ):
        """Сохранение вычисленных метрик в БД"""
        metrics_data = [
            ("pr_review_time", "Среднее время до первого ревью PR", avg_pr_review_time),
            ("pr_approval_time", "Среднее время до одобрения PR", avg_pr_approval_time),
            ("pr_merge_time", "Среднее время до мерджа PR", avg_pr_merge_time),
            ("issue_start_time", "Среднее время до начала работы над задачей", avg_issue_start_time),
            ("issue_completion_time", "Среднее время выполнения задачи", avg_issue_completion_time),
        ]

        for metric_type, metric_name, value in metrics_data:
            if value is not None:
                metric = Metric(
                    project_id=project_id,
                    metric_type=metric_type,
                    metric_name=metric_name,
                    value=value,
                    calculated_at=datetime.utcnow()
                )
                db.add(metric)
        
        db.commit()
