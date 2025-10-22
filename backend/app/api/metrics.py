from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.models.database_models import Metric
from app.models.schemas import BottleneckAnalysis, MetricResponse
from app.services.bottleneck_service import BottleneckService

router = APIRouter(prefix="/metrics", tags=["Metrics"])


@router.get("/bottlenecks/{project_id}", response_model=BottleneckAnalysis)
def analyze_bottlenecks(project_id: int, db: Session = Depends(get_db)):
    """Анализ узких мест проекта"""
    try:
        analysis = BottleneckService.analyze_project(db, project_id)
        return analysis
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/project/{project_id}", response_model=List[MetricResponse])
def get_project_metrics(project_id: int, db: Session = Depends(get_db)):
    """Получение всех метрик проекта"""
    metrics = db.query(Metric).filter(Metric.project_id == project_id).order_by(Metric.calculated_at.desc()).all()
    return metrics
