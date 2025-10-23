"""
Сервис для анализа узких мест в работе над проектом.
Service for analyzing project workflow bottlenecks.
"""
from typing import Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Project, Task


class ProjectBottleneckService:
    """Сервис для анализа узких мест в workflow проекта."""

    @staticmethod
    def analyze_bottlenecks(
        db: Session,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Optional[Dict]:
        """
        Анализ узких мест в workflow проекта.
        Analyze project workflow bottlenecks.
        """
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            return None
        
        # Получить задачи проекта
        tasks = db.query(Task).filter(
            Task.project_id == project_id,
            Task.created_at.between(period_start, period_end)
        ).all()
        
        if not tasks:
            return {
                "project_id": project_id,
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
        
        # Найти узкое место (этап с максимальным временем)
        bottleneck_stage = max(avg_stage_times.items(), key=lambda x: x[1])[0] if avg_stage_times else "none"
        avg_time_in_stage = avg_stage_times.get(bottleneck_stage, 0.0)
        
        # Подсчитать затронутые задачи
        affected_tasks_count = len(stage_times.get(bottleneck_stage, []))
        
        # Рассчитать оценку влияния (0-100)
        # Чем больше время и задач, тем выше влияние
        if bottleneck_stage != "none":
            time_impact = min(50, (avg_time_in_stage / 24) * 10)  # До 50 баллов за время
            task_impact = min(50, (affected_tasks_count / len(tasks)) * 50)  # До 50 баллов за охват
            impact_score = time_impact + task_impact
        else:
            impact_score = 0.0
        
        # Сформировать рекомендации
        recommendations = []
        
        stage_names = {
            "todo": "TODO (ожидание начала)",
            "development": "Разработка",
            "review": "Ревью кода",
            "testing": "Тестирование"
        }
        
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
            recommendations.append("✓ Нет явных узких мест в workflow. Продолжайте в том же духе!")
        
        # Добавить общие рекомендации
        if impact_score > 70:
            recommendations.append(f"Узкое место на этапе '{stage_names.get(bottleneck_stage, bottleneck_stage)}' серьёзно влияет на производительность проекта.")
        
        return {
            "project_id": project_id,
            "bottleneck_stage": bottleneck_stage,
            "avg_time_in_stage": round(avg_time_in_stage, 2),
            "affected_tasks_count": affected_tasks_count,
            "impact_score": round(impact_score, 2),
            "recommendations": recommendations,
            "stage_times": {k: round(v, 2) for k, v in avg_stage_times.items()},
            "period_start": period_start,
            "period_end": period_end,
        }
