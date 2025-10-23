"""
Скрипт для создания демонстрационных проектов с репозиториями и данными.
Script for creating demonstration projects with repositories and data.
"""
import sys
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.models import (
    Project, Repository, ProjectMember, Commit, PullRequest, CodeReview, Task
)


def create_demo_data(db: Session):
    """Создать демонстрационные данные."""
    
    print("=" * 60)
    print("Создание демонстрационных проектов для Git-Komet")
    print("=" * 60)
    print()
    
    # Проект 1: Git-Komet Platform
    print("Создание проекта 1: Git-Komet Platform...")
    project1 = Project(
        external_id="git-komet-platform",
        name="Git-Komet Platform",
        description="Платформа для анализа эффективности разработки"
    )
    db.add(project1)
    db.flush()
    
    # Репозитории проекта 1
    repo1_1 = Repository(
        project_id=project1.id,
        external_id="git-komet-backend",
        name="Git-Komet Backend",
        description="Backend API сервис",
        url="https://github.com/example/git-komet-backend"
    )
    repo1_2 = Repository(
        project_id=project1.id,
        external_id="git-komet-frontend",
        name="Git-Komet Frontend",
        description="Frontend веб-приложение",
        url="https://github.com/example/git-komet-frontend"
    )
    db.add(repo1_1)
    db.add(repo1_2)
    db.flush()
    
    # Участники проекта 1
    members1 = [
        ProjectMember(
            project_id=project1.id,
            external_id="user1",
            email="alex@example.com",
            name="Алексей Иванов",
            role="Senior Developer"
        ),
        ProjectMember(
            project_id=project1.id,
            external_id="user2",
            email="maria@example.com",
            name="Мария Петрова",
            role="Middle Developer"
        ),
        ProjectMember(
            project_id=project1.id,
            external_id="user3",
            email="igor@example.com",
            name="Игорь Сидоров",
            role="Junior Developer"
        ),
    ]
    for member in members1:
        db.add(member)
    db.flush()
    
    # Создать коммиты для Backend репозитория
    base_date = datetime.utcnow() - timedelta(days=30)
    for i in range(80):
        days_offset = i * 0.375  # ~2.7 коммита в день
        commit_date = base_date + timedelta(days=days_offset)
        commit_date = commit_date.replace(hour=random.randint(9, 22), minute=random.randint(0, 59))
        
        author = random.choice(members1)
        
        hour = commit_date.hour
        is_after_hours = hour < 9 or hour > 18
        is_weekend = commit_date.weekday() >= 5
        
        commit = Commit(
            external_id=f"commit-backend-{i}",
            repository_id=repo1_1.id,
            author_id=author.id,
            message=f"Backend: {['Add API endpoint', 'Fix bug in', 'Improve', 'Refactor'][i % 4]} {['authentication', 'database', 'services', 'controllers'][i % 4]}",
            author_email=author.email,
            author_name=author.name,
            committed_at=commit_date,
            files_changed=random.randint(1, 5),
            insertions=random.randint(10, 100),
            deletions=random.randint(0, 50),
            has_tests=random.choice([True, False]),
            todo_count=random.randint(0, 2),
            is_churn=random.random() < 0.1,
            is_after_hours=is_after_hours,
            is_weekend=is_weekend
        )
        db.add(commit)
    
    # Создать коммиты для Frontend репозитория
    for i in range(60):
        days_offset = i * 0.5  # 2 коммита в день
        commit_date = base_date + timedelta(days=days_offset)
        commit_date = commit_date.replace(hour=random.randint(10, 20), minute=random.randint(0, 59))
        
        author = random.choice(members1)
        
        hour = commit_date.hour
        is_after_hours = hour < 9 or hour > 18
        is_weekend = commit_date.weekday() >= 5
        
        commit = Commit(
            external_id=f"commit-frontend-{i}",
            repository_id=repo1_2.id,
            author_id=author.id,
            message=f"Frontend: {['Add component', 'Fix styling in', 'Update', 'Refactor'][i % 4]} {['dashboard', 'metrics', 'charts', 'forms'][i % 4]}",
            author_email=author.email,
            author_name=author.name,
            committed_at=commit_date,
            files_changed=random.randint(1, 8),
            insertions=random.randint(20, 150),
            deletions=random.randint(0, 80),
            has_tests=random.choice([True, False]),
            todo_count=random.randint(0, 3),
            is_churn=random.random() < 0.15,
            is_after_hours=is_after_hours,
            is_weekend=is_weekend
        )
        db.add(commit)
    
    db.flush()
    print(f"✓ Проект 1 создан: {project1.name} (ID: {project1.id})")
    print(f"  - Репозиториев: 2")
    print(f"  - Участников: {len(members1)}")
    print(f"  - Коммитов: 140")
    print()
    
    # Проект 2: Legacy System Refactoring
    print("Создание проекта 2: Legacy System Refactoring...")
    project2 = Project(
        external_id="legacy-refactoring",
        name="Legacy System Refactoring",
        description="Проект по рефакторингу устаревшей системы"
    )
    db.add(project2)
    db.flush()
    
    # Репозитории проекта 2
    repo2_1 = Repository(
        project_id=project2.id,
        external_id="legacy-main",
        name="Legacy Main",
        description="Основной репозиторий legacy системы",
        url="https://github.com/example/legacy-main"
    )
    db.add(repo2_1)
    db.flush()
    
    # Участники проекта 2
    members2 = [
        ProjectMember(
            project_id=project2.id,
            external_id="user4",
            email="sergey@example.com",
            name="Сергей Кузнецов",
            role="Tech Lead"
        ),
        ProjectMember(
            project_id=project2.id,
            external_id="user5",
            email="olga@example.com",
            name="Ольга Смирнова",
            role="Senior Developer"
        ),
    ]
    for member in members2:
        db.add(member)
    db.flush()
    
    # Создать коммиты с высоким churn и переработками
    for i in range(50):
        days_offset = i * 0.6
        commit_date = base_date + timedelta(days=days_offset)
        commit_date = commit_date.replace(hour=random.randint(8, 23), minute=random.randint(0, 59))
        
        author = random.choice(members2)
        
        hour = commit_date.hour
        is_after_hours = hour < 9 or hour > 18 or hour > 21
        is_weekend = commit_date.weekday() >= 5
        
        commit = Commit(
            external_id=f"commit-legacy-{i}",
            repository_id=repo2_1.id,
            author_id=author.id,
            message=f"Legacy: {['Refactor', 'Fix critical bug', 'Remove deprecated', 'Update'][i % 4]} {['module', 'service', 'controller', 'model'][i % 4]}",
            author_email=author.email,
            author_name=author.name,
            committed_at=commit_date,
            files_changed=random.randint(3, 15),
            insertions=random.randint(50, 300),
            deletions=random.randint(30, 250),
            has_tests=random.choice([True, False, False]),
            todo_count=random.randint(1, 5),
            is_churn=random.random() < 0.3,  # Высокий churn
            is_after_hours=is_after_hours,
            is_weekend=is_weekend
        )
        db.add(commit)
    
    db.flush()
    print(f"✓ Проект 2 создан: {project2.name} (ID: {project2.id})")
    print(f"  - Репозиториев: 1")
    print(f"  - Участников: {len(members2)}")
    print(f"  - Коммитов: 50 (высокий технический долг)")
    print()
    
    # Проект 3: Mobile App MVP
    print("Создание проекта 3: Mobile App MVP...")
    project3 = Project(
        external_id="mobile-mvp",
        name="Mobile App MVP",
        description="MVP мобильного приложения"
    )
    db.add(project3)
    db.flush()
    
    # Репозитории проекта 3
    repo3_1 = Repository(
        project_id=project3.id,
        external_id="mobile-ios",
        name="Mobile iOS",
        description="iOS приложение",
        url="https://github.com/example/mobile-ios"
    )
    repo3_2 = Repository(
        project_id=project3.id,
        external_id="mobile-android",
        name="Mobile Android",
        description="Android приложение",
        url="https://github.com/example/mobile-android"
    )
    repo3_3 = Repository(
        project_id=project3.id,
        external_id="mobile-api",
        name="Mobile API",
        description="Backend API для мобильных приложений",
        url="https://github.com/example/mobile-api"
    )
    db.add(repo3_1)
    db.add(repo3_2)
    db.add(repo3_3)
    db.flush()
    
    # Участники проекта 3
    members3 = [
        ProjectMember(
            project_id=project3.id,
            external_id="user6",
            email="anna@example.com",
            name="Анна Волкова",
            role="iOS Developer"
        ),
        ProjectMember(
            project_id=project3.id,
            external_id="user7",
            email="dmitry@example.com",
            name="Дмитрий Козлов",
            role="Android Developer"
        ),
        ProjectMember(
            project_id=project3.id,
            external_id="user8",
            email="elena@example.com",
            name="Елена Новикова",
            role="Backend Developer"
        ),
        ProjectMember(
            project_id=project3.id,
            external_id="user9",
            email="victor@example.com",
            name="Виктор Морозов",
            role="Full Stack Developer"
        ),
    ]
    for member in members3:
        db.add(member)
    db.flush()
    
    # Создать коммиты для iOS
    for i in range(40):
        days_offset = i * 0.75
        commit_date = base_date + timedelta(days=days_offset)
        commit_date = commit_date.replace(hour=random.randint(10, 17), minute=random.randint(0, 59))
        
        commit = Commit(
            external_id=f"commit-ios-{i}",
            repository_id=repo3_1.id,
            author_id=members3[0].id,
            message=f"iOS: {['Add', 'Fix', 'Improve', 'Update'][i % 4]} {['UI', 'navigation', 'data layer', 'networking'][i % 4]}",
            author_email=members3[0].email,
            author_name=members3[0].name,
            committed_at=commit_date,
            files_changed=random.randint(1, 6),
            insertions=random.randint(20, 120),
            deletions=random.randint(0, 60),
            has_tests=True,
            todo_count=random.randint(0, 1),
            is_churn=random.random() < 0.05,
            is_after_hours=False,
            is_weekend=False
        )
        db.add(commit)
    
    # Создать коммиты для Android
    for i in range(40):
        days_offset = i * 0.75
        commit_date = base_date + timedelta(days=days_offset)
        commit_date = commit_date.replace(hour=random.randint(10, 17), minute=random.randint(0, 59))
        
        commit = Commit(
            external_id=f"commit-android-{i}",
            repository_id=repo3_2.id,
            author_id=members3[1].id,
            message=f"Android: {['Add', 'Fix', 'Improve', 'Update'][i % 4]} {['activity', 'fragment', 'viewmodel', 'repository'][i % 4]}",
            author_email=members3[1].email,
            author_name=members3[1].name,
            committed_at=commit_date,
            files_changed=random.randint(1, 6),
            insertions=random.randint(20, 120),
            deletions=random.randint(0, 60),
            has_tests=True,
            todo_count=random.randint(0, 1),
            is_churn=random.random() < 0.05,
            is_after_hours=False,
            is_weekend=False
        )
        db.add(commit)
    
    # Создать коммиты для API
    for i in range(30):
        days_offset = i
        commit_date = base_date + timedelta(days=days_offset)
        commit_date = commit_date.replace(hour=random.randint(11, 16), minute=random.randint(0, 59))
        
        author = random.choice([members3[2], members3[3]])
        
        commit = Commit(
            external_id=f"commit-api-{i}",
            repository_id=repo3_3.id,
            author_id=author.id,
            message=f"API: {['Add endpoint', 'Fix', 'Improve', 'Update'][i % 4]} {['users', 'auth', 'content', 'notifications'][i % 4]}",
            author_email=author.email,
            author_name=author.name,
            committed_at=commit_date,
            files_changed=random.randint(1, 4),
            insertions=random.randint(10, 80),
            deletions=random.randint(0, 40),
            has_tests=True,
            todo_count=random.randint(0, 1),
            is_churn=random.random() < 0.05,
            is_after_hours=False,
            is_weekend=False
        )
        db.add(commit)
    
    db.flush()
    print(f"✓ Проект 3 создан: {project3.name} (ID: {project3.id})")
    print(f"  - Репозиториев: 3")
    print(f"  - Участников: {len(members3)}")
    print(f"  - Коммитов: 110 (отличный work-life balance)")
    print()
    
    db.commit()
    
    print("=" * 60)
    print("✓ Все демонстрационные проекты успешно созданы!")
    print("=" * 60)
    print()
    print("Вы можете использовать эти проекты для демонстрации:")
    print("1. Git-Komet Platform - проект с 2 репозиториями (Backend, Frontend)")
    print("2. Legacy System Refactoring - проект с проблемами и высоким техдолгом")
    print("3. Mobile App MVP - проект с 3 репозиториями и отличными метриками")
    print()
    print("Используйте API для получения метрик:")
    print("  GET /api/v1/projects/ - список проектов")
    print("  GET /api/v1/projects/{id}/repositories - репозитории проекта")
    print("  GET /api/v1/metrics/project/{id}/effectiveness - метрики проекта")
    print("  GET /api/v1/metrics/repository/{id}/effectiveness - метрики репозитория")


def main():
    """Main entry point."""
    db = SessionLocal()
    try:
        create_demo_data(db)
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
