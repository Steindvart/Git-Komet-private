from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Project as ProjectModel, Repository as RepositoryModel
from app.schemas.schemas import Project, ProjectCreate, Repository, RepositoryCreate

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


# Repository endpoints
@router.get("/{project_id}/repositories", response_model=List[Repository])
def list_project_repositories(
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all repositories for a project."""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    repositories = db.query(RepositoryModel).filter(
        RepositoryModel.project_id == project_id
    ).offset(skip).limit(limit).all()
    return repositories


@router.post("/{project_id}/repositories", response_model=Repository)
def create_repository(
    project_id: int,
    repository: RepositoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new repository in a project."""
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Check if repository already exists
    existing = db.query(RepositoryModel).filter(
        RepositoryModel.external_id == repository.external_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Repository already exists")
    
    # Ensure project_id matches
    repo_data = repository.dict()
    repo_data["project_id"] = project_id
    
    db_repository = RepositoryModel(**repo_data)
    db.add(db_repository)
    db.commit()
    db.refresh(db_repository)
    return db_repository


@router.get("/{project_id}/repositories/{repository_id}", response_model=Repository)
def get_repository(
    project_id: int,
    repository_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific repository."""
    repository = db.query(RepositoryModel).filter(
        RepositoryModel.id == repository_id,
        RepositoryModel.project_id == project_id
    ).first()
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repository


@router.delete("/{project_id}/repositories/{repository_id}")
def delete_repository(
    project_id: int,
    repository_id: int,
    db: Session = Depends(get_db)
):
    """Delete a repository."""
    repository = db.query(RepositoryModel).filter(
        RepositoryModel.id == repository_id,
        RepositoryModel.project_id == project_id
    ).first()
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    db.delete(repository)
    db.commit()
    return {"message": "Repository deleted successfully"}
