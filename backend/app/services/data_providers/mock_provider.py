"""
Mock-поставщик данных для целей демонстрации.

Этот поставщик генерирует реалистичные mock-данные для симуляции реальной системы Git-репозитория.
Он может быть легко заменен на реальный поставщик (T1DataProvider, GitHubDataProvider и т.д.)
при готовности к продакшену.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session

from .base_provider import BaseDataProvider
from app.models.models import (
    Project, ProjectMember, Commit, PullRequest,
    CodeReview, Task
)


class MockDataProvider(BaseDataProvider):
    """
    Mock-поставщик данных, который генерирует реалистичные тестовые данные.
    
    Симулирует данные из системы Git-репозитория, такой как T1 Сфера.Код,
    GitHub или GitLab. Структура данных соответствует тому, что поступало бы
    из реального API, что упрощает замену этого поставщика на реальный.
    """
    
    def fetch_commits(
        self,
        db: Session,
        team_id: int,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> List[Dict]:
        """Генерировать mock-данные коммитов."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team or not team.members:
            return []
        
        commits = []
        days_range = (period_end - period_start).days
        count = min(50, days_range * 2)  # ~2 коммита в день в среднем
        
        for i in range(count):
            member = random.choice(team.members)
            commit_date = period_start + timedelta(
                seconds=random.randint(0, int((period_end - period_start).total_seconds()))
            )
            
            # Симуляция различных паттернов коммитов
            has_tests = random.random() > 0.4  # 60% имеют тесты
            test_coverage_delta = random.uniform(-2, 5) if has_tests else random.uniform(-5, 0)
            todo_count = random.choice([0, 0, 0, 1, 2, 3])  # В большинстве коммитов нет TODO
            
            # Симуляция code churn (20% коммитов изменяют недавно измененный код)
            is_churn = random.random() > 0.8
            churn_days = random.randint(1, 7) if is_churn else None
            
            # Симуляция work-life balance
            hour = commit_date.hour
            weekday = commit_date.weekday()
            is_after_hours = hour < 9 or hour > 18
            is_weekend = weekday >= 5
            
            commits.append({
                'external_id': f"mock_commit_{team_id}_{project_id}_{i}_{random.randint(1000, 9999)}",
                'author_email': member.email,
                'author_name': member.name,
                'message': f"Mock commit {i}: {random.choice(['Fix bug', 'Add feature', 'Refactor', 'Update tests', 'TODO: Optimize performance'])}",
                'committed_at': commit_date,
                'files_changed': random.randint(1, 10),
                'insertions': random.randint(10, 200),
                'deletions': random.randint(5, 100),
                'has_tests': has_tests,
                'test_coverage_delta': test_coverage_delta,
                'todo_count': todo_count,
                'is_churn': is_churn,
                'churn_days': churn_days,
                'is_after_hours': is_after_hours,
                'is_weekend': is_weekend
            })
        
        return commits
    
    def fetch_pull_requests(
        self,
        db: Session,
        team_id: int,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> List[Dict]:
        """Генерировать mock-данные pull request."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team or not team.members:
            return []
        
        prs = []
        days_range = (period_end - period_start).days
        count = min(20, days_range // 2)  # ~1 PR каждые 2 дня
        
        for i in range(count):
            member = random.choice(team.members)
            created = period_start + timedelta(
                seconds=random.randint(0, int((period_end - period_start).total_seconds()))
            )
            
            # Симуляция времени ревью
            time_to_first_review = random.uniform(1, 72)  # 1-72 часа
            time_to_merge = time_to_first_review + random.uniform(2, 96)
            review_cycles = random.randint(1, 4)
            
            state = random.choice(["merged", "merged", "merged", "open", "closed"])
            merged_at = created + timedelta(hours=time_to_merge) if state == "merged" else None
            
            prs.append({
                'external_id': f"mock_pr_{project_id}_{i}_{random.randint(1000, 9999)}",
                'project_id': project_id,
                'author_email': member.email,
                'title': f"PR {i}: {random.choice(['Feature', 'Bugfix', 'Refactoring', 'Documentation'])}",
                'description': f"Mock pull request {i}",
                'state': state,
                'created_at': created,
                'updated_at': created + timedelta(hours=random.uniform(0, time_to_merge)),
                'merged_at': merged_at,
                'time_to_first_review': time_to_first_review,
                'time_to_merge': time_to_merge if state == "merged" else None,
                'review_cycles': review_cycles,
                'lines_added': random.randint(50, 500),
                'lines_deleted': random.randint(20, 200),
                'files_changed': random.randint(2, 15)
            })
        
        return prs
    
    def fetch_code_reviews(
        self,
        db: Session,
        pull_request_ids: List[int],
        team_id: int
    ) -> List[Dict]:
        """Генерировать mock-данные code review."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team or not team.members:
            return []
        
        reviews = []
        
        for pr_id in pull_request_ids:
            # Каждый PR получает 1-3 ревью
            num_reviews = random.randint(1, 3)
            
            for _ in range(num_reviews):
                reviewer = random.choice(team.members)
                state = random.choice(["approved", "approved", "changes_requested", "commented"])
                
                comments_count = random.randint(0, 12)
                critical_comments = random.randint(0, min(3, comments_count))
                # 30% ревью содержат предложения TODO
                todo_comments = random.randint(0, 3) if random.random() > 0.7 else 0
                
                reviews.append({
                    'pull_request_id': pr_id,
                    'reviewer_email': reviewer.email,
                    'state': state,
                    'created_at': datetime.utcnow() - timedelta(hours=random.uniform(1, 48)),
                    'comments_count': comments_count,
                    'critical_comments': critical_comments,
                    'todo_comments': todo_comments
                })
        
        return reviews
    
    def fetch_tasks(
        self,
        db: Session,
        team_id: int,
        project_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> List[Dict]:
        """Генерировать mock-данные задач с информацией об узких местах."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team or not team.members:
            return []
        
        tasks = []
        days_range = (period_end - period_start).days
        count = min(30, days_range)  # ~1 задача в день
        
        for i in range(count):
            member = random.choice(team.members)
            created = period_start + timedelta(
                seconds=random.randint(0, int((period_end - period_start).total_seconds()))
            )
            
            state = random.choice(["done", "done", "done", "in_review", "in_progress", "todo"])
            priority = random.choice(["low", "medium", "medium", "high", "critical"])
            
            # Симуляция различного времени в разных этапах для отображения узких мест
            time_in_todo = random.uniform(1, 48)
            time_in_development = random.uniform(4, 120)
            
            # Симуляция узкого места в ревью - некоторые задачи застревают в ревью
            if random.random() > 0.3:  # 70% имеют длительное время ревью
                time_in_review = random.uniform(24, 168)  # 1-7 дней
            else:
                time_in_review = random.uniform(2, 24)
            
            time_in_testing = random.uniform(2, 48)
            
            started_at = created + timedelta(hours=time_in_todo)
            completed_at = started_at + timedelta(
                hours=time_in_development + time_in_review + time_in_testing
            ) if state == "done" else None
            
            tasks.append({
                'external_id': f"mock_task_{project_id}_{i}_{random.randint(1000, 9999)}",
                'project_id': project_id,
                'assignee_email': member.email,
                'title': f"Task {i}: {random.choice(['Implement', 'Fix', 'Refactor', 'Test'])} feature",
                'description': f"Mock task {i}",
                'state': state,
                'priority': priority,
                'created_at': created,
                'started_at': started_at,
                'completed_at': completed_at,
                'time_in_todo': time_in_todo,
                'time_in_development': time_in_development,
                'time_in_review': time_in_review,
                'time_in_testing': time_in_testing
            })
        
        return tasks
    
    def populate_data(
        self,
        db: Session,
        team_id: int,
        project_id: int,
        period_start: Optional[datetime] = None,
        period_end: Optional[datetime] = None
    ) -> Dict:
        """
        Заполнить базу данных mock-данными за указанный период.
        
        Симулирует получение данных из реальной системы Git-репозитория.
        """
        # По умолчанию последние 30 дней, если не указано
        if not period_end:
            period_end = datetime.utcnow()
        if not period_start:
            period_start = period_end - timedelta(days=30)
        
        # Получить mock-данные
        commits_data = self.fetch_commits(db, team_id, project_id, period_start, period_end)
        prs_data = self.fetch_pull_requests(db, team_id, project_id, period_start, period_end)
        tasks_data = self.fetch_tasks(db, team_id, project_id, period_start, period_end)
        
        # Сохранить коммиты в базе данных
        commits_created = []
        for commit_data in commits_data:
            # Найти автора по email
            author = db.query(ProjectMember).filter(
                ProjectMember.email == commit_data['author_email']
            ).first()
            
            commit = Commit(
                external_id=commit_data['external_id'],
                author_id=author.id if author else None,
                message=commit_data['message'],
                author_email=commit_data['author_email'],
                author_name=commit_data['author_name'],
                committed_at=commit_data['committed_at'],
                files_changed=commit_data['files_changed'],
                insertions=commit_data['insertions'],
                deletions=commit_data['deletions'],
                has_tests=commit_data['has_tests'],
                test_coverage_delta=commit_data['test_coverage_delta'],
                todo_count=commit_data['todo_count'],
                is_churn=commit_data['is_churn'],
                churn_days=commit_data['churn_days'],
                is_after_hours=commit_data['is_after_hours'],
                is_weekend=commit_data['is_weekend']
            )
            db.add(commit)
            commits_created.append(commit)
        
        db.commit()
        
        # Сохранить pull request в базе данных
        prs_created = []
        for pr_data in prs_data:
            author = db.query(ProjectMember).filter(
                ProjectMember.email == pr_data['author_email']
            ).first()
            
            pr = PullRequest(
                external_id=pr_data['external_id'],
                project_id=pr_data['project_id'],
                author_id=author.id if author else None,
                title=pr_data['title'],
                description=pr_data['description'],
                state=pr_data['state'],
                created_at=pr_data['created_at'],
                updated_at=pr_data['updated_at'],
                merged_at=pr_data['merged_at'],
                time_to_first_review=pr_data['time_to_first_review'],
                time_to_merge=pr_data['time_to_merge'],
                review_cycles=pr_data['review_cycles'],
                lines_added=pr_data['lines_added'],
                lines_deleted=pr_data['lines_deleted'],
                files_changed=pr_data['files_changed']
            )
            db.add(pr)
            prs_created.append(pr)
        
        db.commit()
        
        # Сохранить code review
        pr_ids = [pr.id for pr in prs_created]
        reviews_data = self.fetch_code_reviews(db, pr_ids, team_id)
        reviews_created = []
        
        for review_data in reviews_data:
            reviewer = db.query(ProjectMember).filter(
                ProjectMember.email == review_data['reviewer_email']
            ).first()
            
            review = CodeReview(
                pull_request_id=review_data['pull_request_id'],
                reviewer_id=reviewer.id if reviewer else None,
                state=review_data['state'],
                created_at=review_data['created_at'],
                comments_count=review_data['comments_count'],
                critical_comments=review_data['critical_comments'],
                todo_comments=review_data['todo_comments']
            )
            db.add(review)
            reviews_created.append(review)
        
        db.commit()
        
        # Сохранить задачи
        tasks_created = []
        for task_data in tasks_data:
            assignee = db.query(ProjectMember).filter(
                ProjectMember.email == task_data['assignee_email']
            ).first()
            
            task = Task(
                external_id=task_data['external_id'],
                project_id=task_data['project_id'],
                assignee_id=assignee.id if assignee else None,
                title=task_data['title'],
                description=task_data['description'],
                state=task_data['state'],
                priority=task_data['priority'],
                created_at=task_data['created_at'],
                started_at=task_data['started_at'],
                completed_at=task_data['completed_at'],
                time_in_todo=task_data['time_in_todo'],
                time_in_development=task_data['time_in_development'],
                time_in_review=task_data['time_in_review'],
                time_in_testing=task_data['time_in_testing']
            )
            db.add(task)
            tasks_created.append(task)
        
        db.commit()
        
        return {
            "commits_created": len(commits_created),
            "pull_requests_created": len(prs_created),
            "reviews_created": len(reviews_created),
            "tasks_created": len(tasks_created),
            "message": "Mock-данные успешно сгенерированы"
        }
