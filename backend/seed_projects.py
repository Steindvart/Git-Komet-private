"""
Скрипт для создания демонстрационных проектов с данными.
Script for creating demonstration projects with data.
"""
import sys
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models import (
    Project, ProjectMember, Commit, PullRequest, CodeReview, Task
)


def create_demo_project_1(db: Session):
    """
    Создать демонстрационный проект 1: Активный веб-проект.
    Create demonstration project 1: Active web project.
    """
    print("Создание проекта 1: Git-Komet Web Application...")
    
    # Создать проект
    project = Project(
        external_id="git-komet-web",
        name="Git-Komet Web Application",
        description="Веб-приложение для анализа эффективности команд через Git-метрики. Активный проект с хорошими показателями."
    )
    db.add(project)
    db.flush()
    
    # Создать участников
    members = [
        ProjectMember(
            project_id=project.id,
            external_id="user1",
            email="developer1@example.com",
            name="Алексей Иванов",
            role="Senior Developer"
        ),
        ProjectMember(
            project_id=project.id,
            external_id="user2",
            email="developer2@example.com",
            name="Мария Петрова",
            role="Middle Developer"
        ),
        ProjectMember(
            project_id=project.id,
            external_id="user3",
            email="developer3@example.com",
            name="Игорь Сидоров",
            role="Junior Developer"
        ),
    ]
    
    for member in members:
        db.add(member)
    db.flush()
    
    # Создать коммиты
    base_date = datetime.utcnow() - timedelta(days=30)
    for i in range(120):
        days_offset = i * 0.25  # 4 коммита в день
        commit_date = base_date + timedelta(days=days_offset)
        
        author = random.choice(members)
        
        # Определить, коммит в рабочее время или нет
        hour = commit_date.hour
        is_after_hours = hour < 9 or hour > 18
        is_weekend = commit_date.weekday() >= 5
        
        commit = Commit(
            external_id=f"commit-web-{i}",
            author_id=author.id,
            message=f"Feature: Implement {['analytics', 'dashboard', 'metrics', 'api'][i % 4]} functionality",
            author_email=author.email,
            author_name=author.name,
            committed_at=commit_date,
            files_changed=random.randint(1, 8),
            insertions=random.randint(10, 200),
            deletions=random.randint(5, 100),
            has_tests=i % 3 == 0,  # 33% коммитов с тестами
            test_coverage_delta=random.uniform(-2, 3) if i % 3 == 0 else None,
            todo_count=random.randint(0, 2),
            is_churn=i % 10 == 0,  # 10% code churn
            churn_days=random.randint(1, 7) if i % 10 == 0 else None,
            is_after_hours=is_after_hours,
            is_weekend=is_weekend
        )
        db.add(commit)
    
    db.flush()
    
    # Создать PR
    for i in range(25):
        days_offset = i * 1.2
        created_date = base_date + timedelta(days=days_offset)
        
        author = random.choice(members)
        
        pr = PullRequest(
            external_id=f"pr-web-{i}",
            project_id=project.id,
            author_id=author.id,
            title=f"Feature: Add {['user', 'admin', 'analytics', 'export'][i % 4]} functionality",
            description=f"Implementation of {['user management', 'admin panel', 'analytics dashboard', 'data export'][i % 4]}",
            state="merged" if i < 20 else "open",
            created_at=created_date,
            updated_at=created_date + timedelta(hours=random.randint(2, 48)),
            merged_at=created_date + timedelta(hours=random.randint(12, 72)) if i < 20 else None,
            time_to_first_review=random.uniform(2, 36),
            time_to_merge=random.uniform(12, 72) if i < 20 else None,
            review_cycles=random.randint(1, 3),
            lines_added=random.randint(50, 500),
            lines_deleted=random.randint(20, 200),
            files_changed=random.randint(3, 15)
        )
        db.add(pr)
        db.flush()
        
        # Добавить ревью
        reviewers = [m for m in members if m.id != author.id]
        for reviewer in random.sample(reviewers, min(2, len(reviewers))):
            review = CodeReview(
                pull_request_id=pr.id,
                reviewer_id=reviewer.id,
                state=random.choice(["approved", "approved", "changes_requested"]),
                created_at=created_date + timedelta(hours=random.randint(2, 24)),
                comments_count=random.randint(1, 8),
                critical_comments=random.randint(0, 2),
                todo_comments=random.randint(0, 3)
            )
            db.add(review)
    
    db.flush()
    
    # Создать задачи
    for i in range(40):
        days_offset = i * 0.75
        created_date = base_date + timedelta(days=days_offset)
        
        assignee = random.choice(members)
        
        state = random.choice(["done", "done", "done", "in_review", "in_progress", "todo"])
        
        task = Task(
            external_id=f"task-web-{i}",
            project_id=project.id,
            assignee_id=assignee.id,
            title=f"Task {i+1}: Implement feature",
            description=f"Detailed description for task {i+1}",
            state=state,
            priority=random.choice(["low", "medium", "high", "critical"]),
            created_at=created_date,
            started_at=created_date + timedelta(hours=random.randint(1, 48)) if state != "todo" else None,
            completed_at=created_date + timedelta(days=random.randint(1, 7)) if state == "done" else None,
            time_in_todo=random.uniform(2, 24),
            time_in_development=random.uniform(8, 48) if state != "todo" else None,
            time_in_review=random.uniform(4, 36) if state in ["in_review", "done"] else None,
            time_in_testing=random.uniform(2, 16) if state == "done" else None
        )
        db.add(task)
    
    db.commit()
    print(f"✓ Проект 1 создан: {project.name} (ID: {project.id})")


def create_demo_project_2(db: Session):
    """
    Создать демонстрационный проект 2: Проект с проблемами.
    Create demonstration project 2: Project with issues.
    """
    print("Создание проекта 2: Legacy System Refactoring...")
    
    # Создать проект
    project = Project(
        external_id="legacy-refactoring",
        name="Legacy System Refactoring",
        description="Рефакторинг легаси-системы. Проект имеет технический долг и узкие места в процессах."
    )
    db.add(project)
    db.flush()
    
    # Создать участников (меньше команда)
    members = [
        ProjectMember(
            project_id=project.id,
            external_id="user4",
            email="developer4@example.com",
            name="Дмитрий Козлов",
            role="Tech Lead"
        ),
        ProjectMember(
            project_id=project.id,
            external_id="user5",
            email="developer5@example.com",
            name="Елена Волкова",
            role="Senior Developer"
        ),
    ]
    
    for member in members:
        db.add(member)
    db.flush()
    
    # Создать коммиты (больше переработок и выходных)
    base_date = datetime.utcnow() - timedelta(days=30)
    for i in range(80):
        days_offset = i * 0.375
        commit_date = base_date + timedelta(days=days_offset)
        
        author = random.choice(members)
        
        # Больше коммитов вне рабочего времени
        hour = commit_date.hour
        is_after_hours = hour < 9 or hour > 18 or random.random() < 0.4  # 40% шанс переработки
        is_weekend = commit_date.weekday() >= 5 or random.random() < 0.25  # 25% шанс работы в выходные
        
        commit = Commit(
            external_id=f"commit-legacy-{i}",
            author_id=author.id,
            message=f"Refactor: Update {['database', 'api', 'ui', 'backend'][i % 4]} code",
            author_email=author.email,
            author_name=author.name,
            committed_at=commit_date,
            files_changed=random.randint(5, 20),
            insertions=random.randint(50, 500),
            deletions=random.randint(30, 400),
            has_tests=i % 5 == 0,  # Только 20% с тестами
            test_coverage_delta=random.uniform(-5, 1) if i % 5 == 0 else None,
            todo_count=random.randint(1, 5),  # Больше TODO
            is_churn=i % 4 == 0,  # 25% code churn (высокий)
            churn_days=random.randint(1, 3) if i % 4 == 0 else None,
            is_after_hours=is_after_hours,
            is_weekend=is_weekend
        )
        db.add(commit)
    
    db.flush()
    
    # Создать PR (меньше, но с долгим ревью)
    for i in range(15):
        days_offset = i * 2
        created_date = base_date + timedelta(days=days_offset)
        
        author = random.choice(members)
        
        pr = PullRequest(
            external_id=f"pr-legacy-{i}",
            project_id=project.id,
            author_id=author.id,
            title=f"Refactor: Modernize {['module', 'service', 'component', 'controller'][i % 4]}",
            description=f"Refactoring {['module', 'service', 'component', 'controller'][i % 4]}",
            state="merged" if i < 12 else "open",
            created_at=created_date,
            updated_at=created_date + timedelta(hours=random.randint(24, 120)),
            merged_at=created_date + timedelta(hours=random.randint(72, 168)) if i < 12 else None,
            time_to_first_review=random.uniform(24, 72),  # Долгое ревью
            time_to_merge=random.uniform(72, 168) if i < 12 else None,
            review_cycles=random.randint(2, 5),  # Много циклов
            lines_added=random.randint(200, 1000),
            lines_deleted=random.randint(100, 800),
            files_changed=random.randint(10, 40)
        )
        db.add(pr)
        db.flush()
        
        # Добавить ревью (много комментариев)
        reviewers = [m for m in members if m.id != author.id]
        for reviewer in reviewers:
            review = CodeReview(
                pull_request_id=pr.id,
                reviewer_id=reviewer.id,
                state=random.choice(["changes_requested", "changes_requested", "approved"]),
                created_at=created_date + timedelta(hours=random.randint(24, 72)),
                comments_count=random.randint(8, 20),  # Много комментариев
                critical_comments=random.randint(2, 5),
                todo_comments=random.randint(3, 8)
            )
            db.add(review)
    
    db.flush()
    
    # Создать задачи (узкое место в ревью)
    for i in range(25):
        days_offset = i * 1.2
        created_date = base_date + timedelta(days=days_offset)
        
        assignee = random.choice(members)
        
        state = random.choice(["done", "in_review", "in_review", "in_progress", "todo"])
        
        task = Task(
            external_id=f"task-legacy-{i}",
            project_id=project.id,
            assignee_id=assignee.id,
            title=f"Refactoring task {i+1}",
            description=f"Refactor legacy code for task {i+1}",
            state=state,
            priority=random.choice(["medium", "high", "high", "critical"]),
            created_at=created_date,
            started_at=created_date + timedelta(hours=random.randint(12, 72)) if state != "todo" else None,
            completed_at=created_date + timedelta(days=random.randint(5, 14)) if state == "done" else None,
            time_in_todo=random.uniform(12, 72),  # Долгое ожидание
            time_in_development=random.uniform(24, 96) if state != "todo" else None,
            time_in_review=random.uniform(48, 120) if state in ["in_review", "done"] else None,  # УЗКОЕ МЕСТО
            time_in_testing=random.uniform(8, 24) if state == "done" else None
        )
        db.add(task)
    
    db.commit()
    print(f"✓ Проект 2 создан: {project.name} (ID: {project.id})")


def create_demo_project_3(db: Session):
    """
    Создать демонстрационный проект 3: Новый стартап проект.
    Create demonstration project 3: New startup project.
    """
    print("Создание проекта 3: Mobile App MVP...")
    
    # Создать проект
    project = Project(
        external_id="mobile-app-mvp",
        name="Mobile App MVP",
        description="Разработка MVP мобильного приложения. Быстрый темп, небольшая команда, отличные показатели."
    )
    db.add(project)
    db.flush()
    
    # Создать участников
    members = [
        ProjectMember(
            project_id=project.id,
            external_id="user6",
            email="developer6@example.com",
            name="Анна Смирнова",
            role="Full Stack Developer"
        ),
        ProjectMember(
            project_id=project.id,
            external_id="user7",
            email="developer7@example.com",
            name="Павел Морозов",
            role="Mobile Developer"
        ),
        ProjectMember(
            project_id=project.id,
            external_id="user8",
            email="developer8@example.com",
            name="Ольга Кузнецова",
            role="UI/UX Developer"
        ),
        ProjectMember(
            project_id=project.id,
            external_id="user9",
            email="developer9@example.com",
            name="Виктор Новиков",
            role="Backend Developer"
        ),
    ]
    
    for member in members:
        db.add(member)
    db.flush()
    
    # Создать коммиты (активные, хороший баланс)
    base_date = datetime.utcnow() - timedelta(days=30)
    for i in range(150):
        days_offset = i * 0.2
        commit_date = base_date + timedelta(days=days_offset)
        
        author = random.choice(members)
        
        # Хороший work-life balance
        hour = commit_date.hour
        is_after_hours = (hour < 9 or hour > 18) and random.random() < 0.15  # Только 15%
        is_weekend = commit_date.weekday() >= 5 and random.random() < 0.1  # Только 10%
        
        commit = Commit(
            external_id=f"commit-mobile-{i}",
            author_id=author.id,
            message=f"Feature: Add {['auth', 'profile', 'feed', 'chat'][i % 4]} screen",
            author_email=author.email,
            author_name=author.name,
            committed_at=commit_date,
            files_changed=random.randint(2, 10),
            insertions=random.randint(20, 250),
            deletions=random.randint(10, 150),
            has_tests=i % 2 == 0,  # 50% с тестами
            test_coverage_delta=random.uniform(0, 5) if i % 2 == 0 else None,
            todo_count=random.randint(0, 1),
            is_churn=i % 15 == 0,  # 6.7% code churn (низкий)
            churn_days=random.randint(5, 14) if i % 15 == 0 else None,
            is_after_hours=is_after_hours,
            is_weekend=is_weekend
        )
        db.add(commit)
    
    db.flush()
    
    # Создать PR (быстрое ревью)
    for i in range(30):
        days_offset = i * 1.0
        created_date = base_date + timedelta(days=days_offset)
        
        author = random.choice(members)
        
        pr = PullRequest(
            external_id=f"pr-mobile-{i}",
            project_id=project.id,
            author_id=author.id,
            title=f"Feature: Implement {['authentication', 'user profile', 'news feed', 'messaging'][i % 4]}",
            description=f"MVP implementation of {['authentication', 'user profile', 'news feed', 'messaging'][i % 4]}",
            state="merged" if i < 27 else "open",
            created_at=created_date,
            updated_at=created_date + timedelta(hours=random.randint(4, 24)),
            merged_at=created_date + timedelta(hours=random.randint(8, 36)) if i < 27 else None,
            time_to_first_review=random.uniform(1, 12),  # Быстрое ревью
            time_to_merge=random.uniform(8, 36) if i < 27 else None,
            review_cycles=random.randint(1, 2),
            lines_added=random.randint(50, 400),
            lines_deleted=random.randint(20, 150),
            files_changed=random.randint(4, 12)
        )
        db.add(pr)
        db.flush()
        
        # Добавить ревью
        reviewers = [m for m in members if m.id != author.id]
        for reviewer in random.sample(reviewers, min(2, len(reviewers))):
            review = CodeReview(
                pull_request_id=pr.id,
                reviewer_id=reviewer.id,
                state=random.choice(["approved", "approved", "approved", "changes_requested"]),
                created_at=created_date + timedelta(hours=random.randint(1, 12)),
                comments_count=random.randint(2, 6),
                critical_comments=random.randint(0, 1),
                todo_comments=random.randint(0, 2)
            )
            db.add(review)
    
    db.flush()
    
    # Создать задачи (хорошо сбалансированы)
    for i in range(50):
        days_offset = i * 0.6
        created_date = base_date + timedelta(days=days_offset)
        
        assignee = random.choice(members)
        
        state = random.choice(["done", "done", "done", "done", "in_review", "in_progress", "todo"])
        
        task = Task(
            external_id=f"task-mobile-{i}",
            project_id=project.id,
            assignee_id=assignee.id,
            title=f"MVP Task {i+1}",
            description=f"MVP task for feature {i+1}",
            state=state,
            priority=random.choice(["medium", "medium", "high", "critical"]),
            created_at=created_date,
            started_at=created_date + timedelta(hours=random.randint(2, 24)) if state != "todo" else None,
            completed_at=created_date + timedelta(days=random.randint(2, 5)) if state == "done" else None,
            time_in_todo=random.uniform(2, 16),
            time_in_development=random.uniform(12, 36) if state != "todo" else None,
            time_in_review=random.uniform(6, 24) if state in ["in_review", "done"] else None,
            time_in_testing=random.uniform(4, 12) if state == "done" else None
        )
        db.add(task)
    
    db.commit()
    print(f"✓ Проект 3 создан: {project.name} (ID: {project.id})")


def main():
    """Главная функция для создания всех демонстрационных проектов."""
    print("\n" + "="*60)
    print("Создание демонстрационных проектов для Git-Komet")
    print("="*60 + "\n")
    
    db = SessionLocal()
    try:
        # Создать три демонстрационных проекта
        create_demo_project_1(db)
        create_demo_project_2(db)
        create_demo_project_3(db)
        
        print("\n" + "="*60)
        print("✓ Все демонстрационные проекты успешно созданы!")
        print("="*60)
        print("\nВы можете использовать эти проекты для демонстрации:")
        print("1. Git-Komet Web Application - активный проект с хорошими показателями")
        print("2. Legacy System Refactoring - проект с проблемами и узкими местами")
        print("3. Mobile App MVP - быстрый стартап с отличными метриками")
        print("\nИспользуйте API для получения метрик проектов:")
        print("  GET /api/v1/metrics/project/{id}/effectiveness")
        print("  GET /api/v1/metrics/project/{id}/technical-debt")
        print("  GET /api/v1/metrics/project/{id}/bottlenecks")
        print("  GET /api/v1/metrics/project/{id}/employee-care")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Ошибка при создании проектов: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
