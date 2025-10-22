from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.database_models import PullRequest
from app.models.schemas import PullRequestCreate, PullRequestResponse

router = APIRouter(prefix="/pull-requests", tags=["Pull Requests"])


@router.post("/", response_model=PullRequestResponse)
def create_pull_request(pr: PullRequestCreate, db: Session = Depends(get_db)):
    """Создание нового Pull Request"""
    db_pr = PullRequest(**pr.dict())
    db.add(db_pr)
    db.commit()
    db.refresh(db_pr)
    return db_pr


@router.get("/project/{project_id}", response_model=List[PullRequestResponse])
def list_pull_requests(project_id: int, db: Session = Depends(get_db)):
    """Получение списка всех Pull Requests проекта"""
    prs = db.query(PullRequest).filter(PullRequest.project_id == project_id).all()
    return prs
