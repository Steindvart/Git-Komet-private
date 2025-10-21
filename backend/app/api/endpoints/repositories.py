from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Project as ProjectModel
from app.schemas.schemas import Project, ProjectCreate
from app.services.data_providers import DataProviderFactory

router = APIRouter()


@router.get("/", response_model=List[Project])
def list_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all projects."""
    projects = db.query(ProjectModel).offset(skip).limit(limit).all()
    return projects


@router.post("/", response_model=Project)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """Create a new project."""
    # Check if project already exists
    existing = db.query(ProjectModel).filter(
        ProjectModel.external_id == project.external_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Project already exists")
    
    db_project = ProjectModel(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


@router.get("/{project_id}", response_model=Project)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific project."""
    project = db.query(ProjectModel).filter(
        ProjectModel.id == project_id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """Delete a project."""
    project = db.query(ProjectModel).filter(
        ProjectModel.id == project_id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}


@router.post("/{project_id}/generate-mock-data")
def generate_mock_data(
    project_id: int,
    team_id: int,
    db: Session = Depends(get_db)
):
    """
    Сгенерировать данные для проекта, используя настроенного поставщика данных.
    
    В настоящее время использует mock-поставщика данных для демонстрации.
    Это симулирует получение:
    - Коммитов с отслеживанием покрытия тестами и TODO
    - Pull request с временем ревью
    - Code review с количеством комментариев
    - Задач с таймингом этапов для анализа узких мест
    
    В продакшене поставщик данных может быть легко заменен на реальный
    (например, T1DataProvider, GitHubDataProvider) через конфигурацию.
    
    Поставщик может быть изменен в коде:
        DataProviderFactory.set_default('t1')  # После реализации
    
    Или можно запросить конкретного поставщика:
        provider = DataProviderFactory.create('github')  # После реализации
    """
    project = db.query(ProjectModel).filter(
        ProjectModel.id == project_id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        # Получить настроенного поставщика данных (по умолчанию 'mock')
        provider = DataProviderFactory.create()
        
        # Использовать поставщика для заполнения данных
        result = provider.populate_data(db, team_id, project_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating data: {str(e)}")
