from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.database_models import Project, PullRequest, Issue
from app.mock_data.generator import MockDataGenerator

router = APIRouter(prefix="/mock", tags=["Mock Data"])


@router.post("/generate")
def generate_mock_data(db: Session = Depends(get_db)):
    """
    Генерация моковых данных для демонстрации.
    Создаёт демо-проект с PR и задачами.
    """
    # Проверяем, есть ли уже демо-проект
    existing_project = db.query(Project).filter(Project.name == "Demo Project").first()
    if existing_project:
        return {
            "message": "Mock data already exists",
            "project_id": existing_project.id,
            "note": "Use DELETE /mock/clear to remove existing data first"
        }
    
    # Создаём проект
    project_data = MockDataGenerator.generate_project()
    project = Project(**project_data.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    
    # Создаём Pull Requests
    prs_data = MockDataGenerator.generate_pull_requests(project.id, count=20)
    for pr_data in prs_data:
        pr = PullRequest(**pr_data.dict())
        db.add(pr)
    
    # Создаём Issues
    issues_data = MockDataGenerator.generate_issues(project.id, count=30)
    for issue_data in issues_data:
        issue = Issue(**issue_data.dict())
        db.add(issue)
    
    db.commit()
    
    return {
        "message": "Mock data generated successfully",
        "project_id": project.id,
        "project_name": project.name,
        "pull_requests_count": len(prs_data),
        "issues_count": len(issues_data)
    }


@router.delete("/clear")
def clear_mock_data(db: Session = Depends(get_db)):
    """Удаление всех моковых данных"""
    # Удаляем в правильном порядке из-за foreign keys
    db.query(PullRequest).delete()
    db.query(Issue).delete()
    db.query(Project).delete()
    db.commit()
    
    return {"message": "All mock data cleared"}
