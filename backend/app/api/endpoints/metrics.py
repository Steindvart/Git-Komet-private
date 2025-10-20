from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from app.db.session import get_db
from app.schemas.schemas import TeamEffectivenessMetrics, RepositoryMetrics
from app.services.metrics_service import MetricsService

router = APIRouter()


@router.get("/team/{team_id}/effectiveness", response_model=TeamEffectivenessMetrics)
def get_team_effectiveness(
    team_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get team effectiveness metrics for a specific period."""
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    metrics = MetricsService.calculate_team_effectiveness(
        db, team_id, period_start, period_end
    )
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return metrics


@router.get("/repository/{repository_id}", response_model=RepositoryMetrics)
def get_repository_metrics(
    repository_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get repository metrics for a specific period."""
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    metrics = MetricsService.calculate_repository_metrics(
        db, repository_id, period_start, period_end
    )
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    return metrics


@router.post("/repository/{repository_id}/calculate")
def calculate_and_save_metrics(
    repository_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Calculate and save repository metrics."""
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    metrics = MetricsService.calculate_repository_metrics(
        db, repository_id, period_start, period_end
    )
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Save metric to database
    saved_metric = MetricsService.save_metric(
        db=db,
        repository_id=repository_id,
        metric_type="repository_metrics",
        metric_value=metrics,
        period_start=period_start,
        period_end=period_end
    )
    
    return {
        "message": "Metrics calculated and saved",
        "metric_id": saved_metric.id,
        "metrics": metrics
    }
