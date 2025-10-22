from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.database_models import Issue
from app.models.schemas import IssueCreate, IssueResponse

router = APIRouter(prefix="/issues", tags=["Issues"])


@router.post("/", response_model=IssueResponse)
def create_issue(issue: IssueCreate, db: Session = Depends(get_db)):
    """Создание новой задачи"""
    db_issue = Issue(**issue.dict())
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


@router.get("/project/{project_id}", response_model=List[IssueResponse])
def list_issues(project_id: int, db: Session = Depends(get_db)):
    """Получение списка всех задач проекта"""
    issues = db.query(Issue).filter(Issue.project_id == project_id).all()
    return issues
