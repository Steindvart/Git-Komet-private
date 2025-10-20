from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Repository as RepositoryModel
from app.schemas.schemas import Repository, RepositoryCreate, RepositoryUpdate
from app.services.git_service import GitService
import os
import tempfile

router = APIRouter()


@router.get("/", response_model=List[Repository])
def list_repositories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all repositories."""
    repositories = db.query(RepositoryModel).offset(skip).limit(limit).all()
    return repositories


@router.post("/", response_model=Repository)
def create_repository(
    repository: RepositoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new repository."""
    # Check if repository already exists
    existing = db.query(RepositoryModel).filter(
        RepositoryModel.url == repository.url
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Repository already exists")
    
    db_repository = RepositoryModel(**repository.dict())
    db.add(db_repository)
    db.commit()
    db.refresh(db_repository)
    return db_repository


@router.get("/{repository_id}", response_model=Repository)
def get_repository(
    repository_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific repository."""
    repository = db.query(RepositoryModel).filter(
        RepositoryModel.id == repository_id
    ).first()
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repository


@router.put("/{repository_id}", response_model=Repository)
def update_repository(
    repository_id: int,
    repository: RepositoryUpdate,
    db: Session = Depends(get_db)
):
    """Update a repository."""
    db_repository = db.query(RepositoryModel).filter(
        RepositoryModel.id == repository_id
    ).first()
    if not db_repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    update_data = repository.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_repository, field, value)
    
    db.commit()
    db.refresh(db_repository)
    return db_repository


@router.delete("/{repository_id}")
def delete_repository(
    repository_id: int,
    db: Session = Depends(get_db)
):
    """Delete a repository."""
    repository = db.query(RepositoryModel).filter(
        RepositoryModel.id == repository_id
    ).first()
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    db.delete(repository)
    db.commit()
    return {"message": "Repository deleted successfully"}


@router.post("/{repository_id}/sync")
def sync_repository(
    repository_id: int,
    db: Session = Depends(get_db)
):
    """Sync repository commits from Git."""
    repository = db.query(RepositoryModel).filter(
        RepositoryModel.id == repository_id
    ).first()
    if not repository:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    try:
        # Create temporary directory for cloning
        with tempfile.TemporaryDirectory() as temp_dir:
            local_path = os.path.join(temp_dir, "repo")
            
            # Clone or open repository
            git_repo = GitService.clone_or_open_repository(repository.url, local_path)
            
            # Extract commits
            commits_data = GitService.extract_commits(git_repo)
            
            # Save to database
            saved_count = GitService.save_commits_to_db(db, repository_id, commits_data)
        
        return {
            "message": "Repository synced successfully",
            "commits_processed": len(commits_data),
            "commits_saved": saved_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error syncing repository: {str(e)}")
