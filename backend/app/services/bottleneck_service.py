from typing import Dict, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Team, TeamMember, Task, PullRequest


class BottleneckService:
    """Service for analyzing workflow bottlenecks."""

    @staticmethod
    def analyze_bottlenecks(
        db: Session,
        team_id: int,
        period_start: datetime,
        period_end: datetime,
        project_id: int = None
    ) -> Dict:
        """Analyze workflow bottlenecks by stage."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            return None
        
        member_ids = [m.id for m in team.members]
        
        # Get tasks for the team
        task_query = db.query(Task).filter(
            Task.assignee_id.in_(member_ids),
            Task.created_at.between(period_start, period_end)
        )
        if project_id:
            task_query = task_query.filter(Task.project_id == project_id)
        tasks = task_query.all()
        
        # Get pull requests
        pr_query = db.query(PullRequest).filter(
            PullRequest.author_id.in_(member_ids),
            PullRequest.created_at.between(period_start, period_end)
        )
        if project_id:
            pr_query = pr_query.filter(PullRequest.project_id == project_id)
        prs = pr_query.all()
        
        if not tasks and not prs:
            return {
                "team_id": team_id,
                "bottleneck_stage": "none",
                "avg_time_in_stage": 0,
                "affected_tasks_count": 0,
                "impact_score": 0,
                "recommendations": ["Нет данных за указанный период"],
                "period_start": period_start.isoformat(),
                "period_end": period_end.isoformat(),
            }
        
        # Calculate average time in each stage
        stages = {
            "todo": [],
            "development": [],
            "review": [],
            "testing": []
        }
        
        for task in tasks:
            if task.time_in_todo:
                stages["todo"].append(task.time_in_todo)
            if task.time_in_development:
                stages["development"].append(task.time_in_development)
            if task.time_in_review:
                stages["review"].append(task.time_in_review)
            if task.time_in_testing:
                stages["testing"].append(task.time_in_testing)
        
        # Add PR review times to review stage
        for pr in prs:
            if pr.time_to_first_review:
                stages["review"].append(pr.time_to_first_review)
        
        # Calculate averages
        stage_averages = {}
        for stage, times in stages.items():
            if times:
                stage_averages[stage] = sum(times) / len(times)
            else:
                stage_averages[stage] = 0
        
        # Find bottleneck (stage with highest average time)
        if stage_averages:
            bottleneck_stage = max(stage_averages, key=stage_averages.get)
            avg_time_in_stage = stage_averages[bottleneck_stage]
        else:
            bottleneck_stage = "none"
            avg_time_in_stage = 0
        
        # Count affected tasks
        affected_tasks_count = len(stages.get(bottleneck_stage, []))
        
        # Calculate impact score (0-100, higher means more severe bottleneck)
        if avg_time_in_stage == 0:
            impact_score = 0
        else:
            # Impact based on time and number of affected items
            time_impact = min(100, (avg_time_in_stage / 24) * 20)  # Per day
            volume_impact = min(50, affected_tasks_count * 5)
            impact_score = time_impact + volume_impact
        
        # Generate recommendations
        recommendations = []
        
        if bottleneck_stage == "review":
            recommendations.append(
                f"⚠️ Ревью кода — узкое место (среднее время {avg_time_in_stage:.1f} часов). "
                "Рассмотрите: увеличение мощности ревьюеров, установку SLA для ревью или внедрение автоматических проверок."
            )
            if avg_time_in_stage > 48:
                recommendations.append(
                    "Ревью занимает более 2 дней в среднем. "
                    "Убедитесь, что члены команды получают уведомления о pending ревью и приоритизируют задачи ревью."
                )
        elif bottleneck_stage == "development":
            recommendations.append(
                f"⚠️ Этап разработки занимает много времени (среднее время {avg_time_in_stage:.1f} часов). "
                "Рассмотрите: декомпозицию задач, парное программирование или работу с техническим долгом."
            )
        elif bottleneck_stage == "testing":
            recommendations.append(
                f"⚠️ Тестирование — узкое место (среднее время {avg_time_in_stage:.1f} часов). "
                "Рассмотрите: увеличение автоматизации тестов, параллельное тестирование или добавление QA ресурсов."
            )
        elif bottleneck_stage == "todo":
            recommendations.append(
                f"Задачи долго ожидают начала работы (среднее время {avg_time_in_stage:.1f} часов). "
                "Пересмотрите приоритизацию беклога и загруженность команды."
            )
        
        if impact_score > 70:
            recommendations.append(
                "🚨 Обнаружено узкое место с высоким влиянием. Рекомендуется немедленное действие для улучшения рабочего процесса."
            )
        elif impact_score > 40:
            recommendations.append(
                "⚠️ Обнаружено умеренное узкое место. Рассмотрите улучшения процесса."
            )
        
        if not recommendations:
            recommendations.append("Значительных узких мест не обнаружено. Рабочий процесс идёт гладко.")
        
        # Add stage-specific metrics
        stage_breakdown = {
            stage: {
                "avg_time": round(avg, 2),
                "count": len(stages[stage])
            }
            for stage, avg in stage_averages.items()
        }
        
        return {
            "team_id": team_id,
            "bottleneck_stage": bottleneck_stage,
            "avg_time_in_stage": round(avg_time_in_stage, 2),
            "affected_tasks_count": affected_tasks_count,
            "impact_score": round(impact_score, 2),
            "recommendations": recommendations,
            "stage_breakdown": stage_breakdown,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
        }
