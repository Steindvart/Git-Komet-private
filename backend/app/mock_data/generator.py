from datetime import datetime, timedelta
import random
from typing import List
from app.models.schemas import ProjectCreate, PullRequestCreate, IssueCreate


class MockDataGenerator:
    """Генератор моковых данных для демонстрации системы"""

    @staticmethod
    def generate_project() -> ProjectCreate:
        """Генерация моковых данных проекта"""
        return ProjectCreate(
            name="Demo Project",
            description="Демонстрационный проект для анализа метрик Git Komet"
        )

    @staticmethod
    def generate_pull_requests(project_id: int, count: int = 20) -> List[PullRequestCreate]:
        """Генерация моковых Pull Requests"""
        pull_requests = []
        base_date = datetime.utcnow() - timedelta(days=90)
        
        authors = ["developer1", "developer2", "developer3", "developer4"]
        
        for i in range(1, count + 1):
            created_at = base_date + timedelta(days=random.randint(0, 85))
            
            # Симулируем различные сценарии
            scenario = random.choice(["fast", "normal", "slow", "very_slow"])
            
            if scenario == "fast":
                # Быстрое ревью и мердж
                first_review_at = created_at + timedelta(hours=random.randint(1, 4))
                approved_at = first_review_at + timedelta(hours=random.randint(1, 3))
                merged_at = approved_at + timedelta(hours=random.randint(1, 2))
            elif scenario == "normal":
                # Нормальное время
                first_review_at = created_at + timedelta(hours=random.randint(6, 16))
                approved_at = first_review_at + timedelta(hours=random.randint(4, 12))
                merged_at = approved_at + timedelta(hours=random.randint(2, 8))
            elif scenario == "slow":
                # Медленное - узкое место
                first_review_at = created_at + timedelta(hours=random.randint(24, 48))
                approved_at = first_review_at + timedelta(hours=random.randint(24, 48))
                merged_at = approved_at + timedelta(hours=random.randint(12, 24))
            else:  # very_slow
                # Очень медленное - серьёзное узкое место
                first_review_at = created_at + timedelta(hours=random.randint(48, 120))
                approved_at = first_review_at + timedelta(hours=random.randint(48, 96))
                merged_at = approved_at + timedelta(hours=random.randint(24, 48))
            
            pr = PullRequestCreate(
                project_id=project_id,
                pr_number=i,
                title=f"Feature/fix #{i}",
                author=random.choice(authors),
                created_at=created_at,
                first_review_at=first_review_at,
                approved_at=approved_at,
                merged_at=merged_at,
                closed_at=merged_at
            )
            pull_requests.append(pr)
        
        return pull_requests

    @staticmethod
    def generate_issues(project_id: int, count: int = 30) -> List[IssueCreate]:
        """Генерация моковых Issues/задач"""
        issues = []
        base_date = datetime.utcnow() - timedelta(days=90)
        
        authors = ["developer1", "developer2", "developer3", "developer4", "manager1"]
        statuses = ["open", "in_progress", "completed", "closed"]
        
        for i in range(1, count + 1):
            created_at = base_date + timedelta(days=random.randint(0, 85))
            status = random.choice(statuses)
            
            # Симулируем различные сценарии для задач
            scenario = random.choice(["quick", "normal", "delayed", "very_delayed"])
            
            started_at = None
            completed_at = None
            closed_at = None
            
            if status in ["in_progress", "completed", "closed"]:
                if scenario == "quick":
                    # Быстро взяли в работу
                    started_at = created_at + timedelta(hours=random.randint(2, 12))
                elif scenario == "normal":
                    # Нормально
                    started_at = created_at + timedelta(hours=random.randint(12, 36))
                elif scenario == "delayed":
                    # Задержка начала работы - узкое место
                    started_at = created_at + timedelta(hours=random.randint(48, 96))
                else:  # very_delayed
                    # Серьёзная задержка
                    started_at = created_at + timedelta(hours=random.randint(96, 168))
            
            if status in ["completed", "closed"] and started_at:
                # Время выполнения
                if scenario == "quick":
                    completed_at = started_at + timedelta(hours=random.randint(4, 24))
                elif scenario == "normal":
                    completed_at = started_at + timedelta(hours=random.randint(24, 96))
                elif scenario == "delayed":
                    completed_at = started_at + timedelta(hours=random.randint(96, 168))
                else:  # very_delayed
                    completed_at = started_at + timedelta(hours=random.randint(168, 336))
                
                closed_at = completed_at + timedelta(hours=random.randint(1, 4))
            
            issue = IssueCreate(
                project_id=project_id,
                issue_number=i,
                title=f"Task #{i}: Implement feature/Fix bug",
                author=random.choice(authors),
                created_at=created_at,
                started_at=started_at,
                completed_at=completed_at,
                closed_at=closed_at,
                status=status
            )
            issues.append(issue)
        
        return issues
