"""
Сервис для анализа узких мест в работе над репозиторием.
Service for analyzing repository workflow bottlenecks.
"""
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Repository, Task


class RepositoryBottleneckService:
    """Сервис для анализа узких мест в workflow репозитория."""

    @staticmethod
    def analyze_bottlenecks(
        db: Session,
        repository_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Анализ узких мест в workflow репозитория.
        Analyze repository workflow bottlenecks.
        """
        repository = db.query(Repository).filter(Repository.id == repository_id).first()
        if not repository:
            return None
        
        # Получить задачи репозитория
        tasks = db.query(Task).filter(
            Task.repository_id == repository_id,
            Task.created_at.between(period_start, period_end)
        ).all()
        
        if not tasks:
            return {
                "repository_id": repository_id,
                "bottleneck_stage": "none",
                "avg_time_in_stage": 0.0,
                "affected_tasks_count": 0,
                "impact_score": 0.0,
                "recommendations": ["Недостаточно данных для анализа узких мест."],
                "stage_times": {
                    "todo": 0.0,
                    "development": 0.0,
                    "review": 0.0,
                    "testing": 0.0
                },
                "period_start": period_start,
                "period_end": period_end,
            }
        
        # Рассчитать среднее время на каждом этапе
        stage_times = {
            "todo": [],
            "development": [],
            "review": [],
            "testing": []
        }
        
        for task in tasks:
            if task.time_in_todo:
                stage_times["todo"].append(task.time_in_todo)
            if task.time_in_development:
                stage_times["development"].append(task.time_in_development)
            if task.time_in_review:
                stage_times["review"].append(task.time_in_review)
            if task.time_in_testing:
                stage_times["testing"].append(task.time_in_testing)
        
        # Вычислить средние значения
        avg_stage_times = {}
        for stage, times in stage_times.items():
            avg_stage_times[stage] = sum(times) / len(times) if times else 0.0
        
        # Найти узкое место
        bottleneck_stage = max(avg_stage_times.items(), key=lambda x: x[1])[0] if avg_stage_times else "none"
        avg_time_in_stage = avg_stage_times.get(bottleneck_stage, 0.0)
        
        # Подсчитать затронутые задачи
        affected_tasks_count = len(stage_times.get(bottleneck_stage, []))
        
        # Рассчитать оценку влияния
        if bottleneck_stage != "none":
            time_impact = min(50, (avg_time_in_stage / 24) * 10)
            task_impact = min(50, (affected_tasks_count / len(tasks)) * 50)
            impact_score = time_impact + task_impact
        else:
            impact_score = 0.0
        
        # Сформировать рекомендации
        recommendations = []
        
        if bottleneck_stage == "review":
            if avg_time_in_stage > 48:
                recommendations.append("⚠️ Критическое время в ревью (>2 дней). Увеличьте количество ревьюеров или установите SLA.")
            elif avg_time_in_stage > 24:
                recommendations.append("Время в ревью высокое (>1 дня). Рассмотрите оптимизацию процесса ревью.")
            else:
                recommendations.append("Ревью - узкое место, но время приемлемое. Следите за трендом.")
        elif bottleneck_stage == "development":
            if avg_time_in_stage > 72:
                recommendations.append("⚠️ Длительная разработка задач. Возможно, задачи слишком большие - декомпозируйте их.")
            else:
                recommendations.append("Разработка занимает больше всего времени. Это нормально, но можно оптимизировать.")
        elif bottleneck_stage == "testing":
            if avg_time_in_stage > 48:
                recommendations.append("⚠️ Долгое тестирование. Рассмотрите автоматизацию тестов или увеличение QA ресурсов.")
            else:
                recommendations.append("Тестирование - узкое место. Проверьте процессы QA.")
        elif bottleneck_stage == "todo":
            recommendations.append("⚠️ Задачи долго ждут начала работы. Проверьте приоритизацию и загрузку команды.")
        else:
            recommendations.append("✓ Узких мест не обнаружено. Workflow работает эффективно!")
        
        return {
            "repository_id": repository_id,
            "bottleneck_stage": bottleneck_stage,
            "avg_time_in_stage": round(avg_time_in_stage, 2),
            "affected_tasks_count": affected_tasks_count,
            "impact_score": round(impact_score, 2),
            "recommendations": recommendations,
            "stage_times": {k: round(v, 2) for k, v in avg_stage_times.items()},
            "period_start": period_start,
            "period_end": period_end,
        }
