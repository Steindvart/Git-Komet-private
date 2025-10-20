"""
Mock data service to simulate T1 Сфера.Код API responses.
In production, this would be replaced with actual API calls to T1 system.
"""

from typing import List, Dict
from datetime import datetime, timedelta
import random
from app.models.models import (
    Project, Team, TeamMember, Commit, PullRequest, 
    CodeReview, Task
)
from sqlalchemy.orm import Session


class T1MockDataService:
    """Service to generate mock data as if from T1 Сфера.Код API."""

    @staticmethod
    def generate_mock_commits(
        db: Session,
        team_id: int,
        project_id: int,
        count: int = 50,
        days_back: int = 30
    ) -> List[Commit]:
        """Generate mock commit data."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team or not team.members:
            return []
        
        commits = []
        end_date = datetime.utcnow()
        
        for i in range(count):
            member = random.choice(team.members)
            commit_date = end_date - timedelta(days=random.randint(0, days_back))
            
            # Simulate different commit patterns
            has_tests = random.random() > 0.4  # 60% have tests
            test_coverage_delta = random.uniform(-2, 5) if has_tests else random.uniform(-5, 0)
            todo_count = random.choice([0, 0, 0, 1, 2])  # Most commits have no TODOs
            
            commit = Commit(
                external_id=f"mock_commit_{team_id}_{i}_{random.randint(1000, 9999)}",
                author_id=member.id,
                message=f"Mock commit {i}: {random.choice(['Fix bug', 'Add feature', 'Refactor', 'Update tests'])}",
                author_email=member.email,
                author_name=member.name,
                committed_at=commit_date,
                files_changed=random.randint(1, 10),
                insertions=random.randint(10, 200),
                deletions=random.randint(5, 100),
                has_tests=has_tests,
                test_coverage_delta=test_coverage_delta,
                todo_count=todo_count
            )
            db.add(commit)
            commits.append(commit)
        
        db.commit()
        return commits

    @staticmethod
    def generate_mock_pull_requests(
        db: Session,
        team_id: int,
        project_id: int,
        count: int = 20,
        days_back: int = 30
    ) -> List[PullRequest]:
        """Generate mock pull request data."""
        team = db.query(Team).filter(Team.id == team_id).first()
        project = db.query(Project).filter(Project.id == project_id).first()
        
        if not team or not team.members or not project:
            return []
        
        prs = []
        end_date = datetime.utcnow()
        
        for i in range(count):
            member = random.choice(team.members)
            created = end_date - timedelta(days=random.randint(0, days_back))
            
            # Simulate review times
            time_to_first_review = random.uniform(1, 72)  # 1-72 hours
            time_to_merge = time_to_first_review + random.uniform(2, 96)
            review_cycles = random.randint(1, 4)
            
            state = random.choice(["merged", "merged", "merged", "open", "closed"])
            merged_at = created + timedelta(hours=time_to_merge) if state == "merged" else None
            
            pr = PullRequest(
                external_id=f"mock_pr_{project_id}_{i}_{random.randint(1000, 9999)}",
                project_id=project_id,
                author_id=member.id,
                title=f"PR {i}: {random.choice(['Feature', 'Bugfix', 'Refactoring', 'Documentation'])}",
                description=f"Mock pull request {i}",
                state=state,
                created_at=created,
                updated_at=created + timedelta(hours=random.uniform(0, time_to_merge)),
                merged_at=merged_at,
                time_to_first_review=time_to_first_review,
                time_to_merge=time_to_merge if state == "merged" else None,
                review_cycles=review_cycles,
                lines_added=random.randint(50, 500),
                lines_deleted=random.randint(20, 200),
                files_changed=random.randint(2, 15)
            )
            db.add(pr)
            prs.append(pr)
        
        db.commit()
        return prs

    @staticmethod
    def generate_mock_code_reviews(
        db: Session,
        pull_request_ids: List[int],
        team_id: int
    ) -> List[CodeReview]:
        """Generate mock code review data."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team or not team.members:
            return []
        
        reviews = []
        
        for pr_id in pull_request_ids:
            # Each PR gets 1-3 reviews
            num_reviews = random.randint(1, 3)
            
            for _ in range(num_reviews):
                reviewer = random.choice(team.members)
                state = random.choice(["approved", "approved", "changes_requested", "commented"])
                
                comments_count = random.randint(0, 10)
                critical_comments = random.randint(0, min(3, comments_count))
                
                review = CodeReview(
                    pull_request_id=pr_id,
                    reviewer_id=reviewer.id,
                    state=state,
                    created_at=datetime.utcnow() - timedelta(hours=random.uniform(1, 48)),
                    comments_count=comments_count,
                    critical_comments=critical_comments
                )
                db.add(review)
                reviews.append(review)
        
        db.commit()
        return reviews

    @staticmethod
    def generate_mock_tasks(
        db: Session,
        team_id: int,
        project_id: int,
        count: int = 30,
        days_back: int = 30
    ) -> List[Task]:
        """Generate mock task data with bottleneck information."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team or not team.members:
            return []
        
        tasks = []
        end_date = datetime.utcnow()
        
        for i in range(count):
            member = random.choice(team.members)
            created = end_date - timedelta(days=random.randint(0, days_back))
            
            state = random.choice(["done", "done", "done", "in_review", "in_progress", "todo"])
            priority = random.choice(["low", "medium", "medium", "high", "critical"])
            
            # Simulate different stage times to show bottlenecks
            time_in_todo = random.uniform(1, 48)
            time_in_development = random.uniform(4, 120)
            
            # Simulate review bottleneck - some tasks stuck in review
            if random.random() > 0.3:  # 70% have long review times
                time_in_review = random.uniform(24, 168)  # 1-7 days
            else:
                time_in_review = random.uniform(2, 24)
            
            time_in_testing = random.uniform(2, 48)
            
            started_at = created + timedelta(hours=time_in_todo)
            completed_at = started_at + timedelta(
                hours=time_in_development + time_in_review + time_in_testing
            ) if state == "done" else None
            
            task = Task(
                external_id=f"mock_task_{project_id}_{i}_{random.randint(1000, 9999)}",
                project_id=project_id,
                assignee_id=member.id,
                title=f"Task {i}: {random.choice(['Implement', 'Fix', 'Refactor', 'Test'])} feature",
                description=f"Mock task {i}",
                state=state,
                priority=priority,
                created_at=created,
                started_at=started_at,
                completed_at=completed_at,
                time_in_todo=time_in_todo,
                time_in_development=time_in_development,
                time_in_review=time_in_review,
                time_in_testing=time_in_testing
            )
            db.add(task)
            tasks.append(task)
        
        db.commit()
        return tasks

    @staticmethod
    def populate_mock_data(
        db: Session,
        team_id: int,
        project_id: int
    ) -> Dict:
        """Populate database with comprehensive mock data."""
        
        commits = T1MockDataService.generate_mock_commits(db, team_id, project_id)
        prs = T1MockDataService.generate_mock_pull_requests(db, team_id, project_id)
        
        pr_ids = [pr.id for pr in prs]
        reviews = T1MockDataService.generate_mock_code_reviews(db, pr_ids, team_id)
        
        tasks = T1MockDataService.generate_mock_tasks(db, team_id, project_id)
        
        return {
            "commits_created": len(commits),
            "pull_requests_created": len(prs),
            "reviews_created": len(reviews),
            "tasks_created": len(tasks),
            "message": "Mock data from T1 Сфера.Код API generated successfully"
        }
