"""
Тесты для проектных сервисов.
Tests for project services.
"""
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.session import Base
from app.models.models import Project, ProjectMember, Commit, PullRequest, Task, CodeReview
from app.services.project_effectiveness_service import ProjectEffectivenessService
from app.services.project_technical_debt_service import ProjectTechnicalDebtService
from app.services.project_bottleneck_service import ProjectBottleneckService


# Настройка тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_projects.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def test_db():
    """Создать тестовую базу данных."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session(test_db):
    """Получить сессию БД."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def sample_project(db_session):
    """Создать тестовый проект с данными."""
    # Создать проект
    project = Project(
        external_id="test-project",
        name="Test Project",
        description="Test project for unit tests"
    )
    db_session.add(project)
    db_session.flush()
    
    # Создать участников
    member1 = ProjectMember(
        project_id=project.id,
        external_id="user1",
        email="user1@test.com",
        name="Test User 1",
        role="Developer"
    )
    member2 = ProjectMember(
        project_id=project.id,
        external_id="user2",
        email="user2@test.com",
        name="Test User 2",
        role="Developer"
    )
    db_session.add_all([member1, member2])
    db_session.flush()
    
    # Создать коммиты
    base_date = datetime.utcnow() - timedelta(days=15)
    for i in range(20):
        commit = Commit(
            external_id=f"commit-{i}",
            author_id=member1.id if i % 2 == 0 else member2.id,
            message=f"Test commit {i}",
            author_email=member1.email if i % 2 == 0 else member2.email,
            author_name=member1.name if i % 2 == 0 else member2.name,
            committed_at=base_date + timedelta(days=i * 0.5),
            files_changed=3,
            insertions=50,
            deletions=20,
            has_tests=i % 3 == 0,
            todo_count=i % 5,
            is_after_hours=i % 10 == 0,
            is_weekend=i % 15 == 0,
            is_churn=i % 8 == 0
        )
        db_session.add(commit)
    
    # Создать PR
    for i in range(5):
        pr = PullRequest(
            external_id=f"pr-{i}",
            project_id=project.id,
            author_id=member1.id,
            title=f"Test PR {i}",
            state="merged",
            created_at=base_date + timedelta(days=i * 2),
            updated_at=base_date + timedelta(days=i * 2 + 1),
            merged_at=base_date + timedelta(days=i * 2 + 2),
            time_to_first_review=12.0,
            time_to_merge=48.0,
            review_cycles=2,
            lines_added=100,
            lines_deleted=50,
            files_changed=5
        )
        db_session.add(pr)
        db_session.flush()
        
        # Добавить ревью
        review = CodeReview(
            pull_request_id=pr.id,
            reviewer_id=member2.id,
            state="approved",
            created_at=base_date + timedelta(days=i * 2, hours=12),
            comments_count=3,
            critical_comments=1,
            todo_comments=1
        )
        db_session.add(review)
    
    # Создать задачи
    for i in range(10):
        task = Task(
            external_id=f"task-{i}",
            project_id=project.id,
            assignee_id=member1.id if i % 2 == 0 else member2.id,
            title=f"Test task {i}",
            state="done" if i < 7 else "in_progress",
            priority="medium",
            created_at=base_date + timedelta(days=i),
            started_at=base_date + timedelta(days=i, hours=2),
            completed_at=base_date + timedelta(days=i + 2) if i < 7 else None,
            time_in_todo=4.0,
            time_in_development=16.0,
            time_in_review=24.0,
            time_in_testing=8.0
        )
        db_session.add(task)
    
    db_session.commit()
    return project


class TestProjectEffectivenessService:
    """Тесты для сервиса эффективности проекта."""
    
    def test_calculate_effectiveness_score(self, db_session, sample_project):
        """Тест расчёта оценки эффективности (новое ТЗ: без PR и задач)."""
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=30)
        
        result = ProjectEffectivenessService.calculate_effectiveness_score(
            db_session, sample_project.id, period_start, period_end
        )
        
        assert result is not None
        assert result["project_id"] == sample_project.id
        assert result["project_name"] == sample_project.name
        assert 0 <= result["effectiveness_score"] <= 100
        assert result["total_commits"] == 20
        assert result["active_contributors"] == 2
        assert isinstance(result["has_alert"], bool)
    
    def test_calculate_employee_care_metric(self, db_session, sample_project):
        """Тест расчёта метрики заботы о сотрудниках."""
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=30)
        
        result = ProjectEffectivenessService.calculate_employee_care_metric(
            db_session, sample_project.id, period_start, period_end
        )
        
        assert result is not None
        assert result["project_id"] == sample_project.id
        assert 0 <= result["employee_care_score"] <= 100
        assert result["after_hours_percentage"] >= 0
        assert result["weekend_percentage"] >= 0
        assert result["status"] in ["excellent", "good", "needs_attention", "critical"]
        assert isinstance(result["recommendations"], list)
        assert len(result["recommendations"]) > 0
    
    def test_calculate_active_contributors(self, db_session, sample_project):
        """Тест расчёта активных участников (новое ТЗ)."""
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=30)
        
        result = ProjectEffectivenessService.calculate_active_contributors(
            db_session, sample_project.id, period_start, period_end
        )
        
        assert result is not None
        assert result["project_id"] == sample_project.id
        assert result["active_contributors"] == 2
        assert result["total_commits"] == 20
        assert result["avg_commits_per_contributor"] == 10.0
    
    def test_calculate_commits_per_person(self, db_session, sample_project):
        """Тест расчёта коммитов на человека для оценки экспертности (новое ТЗ)."""
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=30)
        
        result = ProjectEffectivenessService.calculate_commits_per_person(
            db_session, sample_project.id, period_start, period_end
        )
        
        assert result is not None
        assert result["project_id"] == sample_project.id
        assert result["total_contributors"] == 2
        assert len(result["contributors"]) == 2
        
        # Проверить структуру данных участника
        contributor = result["contributors"][0]
        assert "author_id" in contributor
        assert "author_name" in contributor
        assert "author_email" in contributor
        assert "commit_count" in contributor
        assert "lines_changed" in contributor
        assert "expertise_level" in contributor
        assert contributor["expertise_level"] in ["beginner", "intermediate", "advanced", "expert"]
    
    def test_nonexistent_project(self, db_session):
        """Тест для несуществующего проекта."""
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=30)
        
        result = ProjectEffectivenessService.calculate_effectiveness_score(
            db_session, 999, period_start, period_end
        )
        
        assert result is None


class TestProjectTechnicalDebtService:
    """Тесты для сервиса технического долга."""
    
    def test_analyze_technical_debt(self, db_session, sample_project):
        """Тест анализа технического долга (новое ТЗ: только TODO)."""
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=30)
        
        result = ProjectTechnicalDebtService.analyze_technical_debt(
            db_session, sample_project.id, period_start, period_end
        )
        
        assert result is not None
        assert result["project_id"] == sample_project.id
        assert result["todo_count"] >= 0
        assert result["todo_trend"] in ["up", "down", "stable"]
        assert 0 <= result["technical_debt_score"] <= 100
        assert isinstance(result["recommendations"], list)
        assert len(result["recommendations"]) > 0
    
    def test_save_technical_debt_metric(self, db_session, sample_project):
        """Тест сохранения метрики технического долга."""
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=30)
        
        metrics = {
            "todo_count": 50,
            "todo_trend": "stable",
            "technical_debt_score": 25.0
        }
        
        saved_metric = ProjectTechnicalDebtService.save_technical_debt_metric(
            db_session, sample_project.id, metrics, period_start, period_end
        )
        
        assert saved_metric is not None
        assert saved_metric.project_id == sample_project.id
        assert saved_metric.todo_count == 50


class TestProjectBottleneckService:
    """Тесты для сервиса узких мест."""
    
    def test_analyze_bottlenecks(self, db_session, sample_project):
        """Тест анализа узких мест."""
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=30)
        
        result = ProjectBottleneckService.analyze_bottlenecks(
            db_session, sample_project.id, period_start, period_end
        )
        
        assert result is not None
        assert result["project_id"] == sample_project.id
        assert result["bottleneck_stage"] in ["todo", "development", "review", "testing", "none"]
        assert result["avg_time_in_stage"] >= 0
        assert result["affected_tasks_count"] >= 0
        assert 0 <= result["impact_score"] <= 100
        assert isinstance(result["recommendations"], list)
        assert isinstance(result["stage_times"], dict)
    
    def test_empty_project(self, db_session):
        """Тест для проекта без данных."""
        # Создать пустой проект
        project = Project(
            external_id="empty-project",
            name="Empty Project",
            description="Project with no data"
        )
        db_session.add(project)
        db_session.commit()
        
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=30)
        
        result = ProjectBottleneckService.analyze_bottlenecks(
            db_session, project.id, period_start, period_end
        )
        
        assert result is not None
        assert result["bottleneck_stage"] == "none"
        assert result["avg_time_in_stage"] == 0.0
        assert result["affected_tasks_count"] == 0
    
    def test_get_prs_needing_attention(self, db_session, sample_project):
        """Тест получения списка PR/MR, требующих внимания."""
        # Создать открытые PR с разным временем на ревью
        base_date = datetime.utcnow()
        
        # PR1: 120 часов на ревью (5 дней) - должен быть в списке
        pr1 = PullRequest(
            external_id="pr-attention-1",
            project_id=sample_project.id,
            author_id=1,
            title="Старый PR требует внимания",
            state="open",
            created_at=base_date - timedelta(hours=120),
            updated_at=base_date - timedelta(hours=120)
        )
        db_session.add(pr1)
        db_session.flush()
        
        # Добавить ревью к PR1
        review1 = CodeReview(
            pull_request_id=pr1.id,
            reviewer_id=1,
            state="changes_requested",
            created_at=base_date - timedelta(hours=118),
            comments_count=5
        )
        db_session.add(review1)
        
        # PR2: 50 часов на ревью (2 дня) - не должен быть в списке при min_hours=96
        pr2 = PullRequest(
            external_id="pr-attention-2",
            project_id=sample_project.id,
            author_id=1,
            title="Относительно свежий PR",
            state="open",
            created_at=base_date - timedelta(hours=50),
            updated_at=base_date - timedelta(hours=50)
        )
        db_session.add(pr2)
        
        # PR3: 10 часов на ревью - не должен быть в списке
        pr3 = PullRequest(
            external_id="pr-attention-3",
            project_id=sample_project.id,
            author_id=1,
            title="Свежий PR",
            state="open",
            created_at=base_date - timedelta(hours=10),
            updated_at=base_date - timedelta(hours=10)
        )
        db_session.add(pr3)
        
        # PR4: закрытый PR - не должен быть в списке
        pr4 = PullRequest(
            external_id="pr-attention-4",
            project_id=sample_project.id,
            author_id=1,
            title="Закрытый PR",
            state="merged",
            created_at=base_date - timedelta(hours=200),
            updated_at=base_date - timedelta(hours=1),
            merged_at=base_date - timedelta(hours=1)
        )
        db_session.add(pr4)
        
        db_session.commit()
        
        # Тест 1: Получить PR с min_hours=96
        result = ProjectBottleneckService.get_prs_needing_attention(
            db_session, sample_project.id, min_hours_in_review=96.0, limit=5
        )
        
        assert result is not None
        assert len(result) == 1
        assert result[0]["title"] == "Старый PR требует внимания"
        assert result[0]["indicator"] == "🌩️"  # > 96 часов
        assert result[0]["time_in_review_hours"] > 96
        
        # Тест 2: Получить все открытые PR с min_hours=0
        result_all = ProjectBottleneckService.get_prs_needing_attention(
            db_session, sample_project.id, min_hours_in_review=0, limit=10
        )
        
        assert result_all is not None
        assert len(result_all) == 3  # pr1, pr2, pr3 (pr4 закрыт)
        
        # Проверить сортировку - самый долгий PR должен быть первым
        assert result_all[0]["title"] == "Старый PR требует внимания"
        
        # Тест 3: Проверить визуальные индикаторы
        indicators = [pr["indicator"] for pr in result_all]
        assert "🌩️" in indicators  # > 96 часов
        assert "🌧️" in indicators  # 24-96 часов
        assert "☀️" in indicators  # < 24 часов
    
    def test_get_prs_needing_attention_empty(self, db_session):
        """Тест для проекта без PR."""
        project = Project(
            external_id="empty-pr-project",
            name="Project without PRs",
            description="Project with no PRs"
        )
        db_session.add(project)
        db_session.commit()
        
        result = ProjectBottleneckService.get_prs_needing_attention(
            db_session, project.id, min_hours_in_review=96.0, limit=5
        )
        
        assert result is not None
        assert len(result) == 0
    
    def test_get_prs_needing_attention_nonexistent_project(self, db_session):
        """Тест для несуществующего проекта."""
        result = ProjectBottleneckService.get_prs_needing_attention(
            db_session, 999999, min_hours_in_review=96.0, limit=5
        )
        
        assert result is None
