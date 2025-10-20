from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Project as ProjectModel
from app.schemas.schemas import Project, ProjectCreate
from app.services.t1_mock_service import T1MockDataService

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
    Generate mock data for a project for demonstration purposes.
    
    This simulates receiving:
    - Commits with test coverage and TODO tracking
    - Pull requests with review times
    - Code reviews with comment counts
    - Tasks with stage timing for bottleneck analysis
    
    In production, this would be replaced with actual Git repository integration.
    """
    project = db.query(ProjectModel).filter(
        ProjectModel.id == project_id
    ).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    try:
        result = T1MockDataService.populate_mock_data(db, team_id, project_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating mock data: {str(e)}")
