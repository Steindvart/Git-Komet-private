from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.session import get_db
from app.schemas.schemas import (
    TeamEffectivenessMetrics,
    TechnicalDebtAnalysis,
    BottleneckAnalysis
)
from app.services.team_effectiveness_service import TeamEffectivenessService
from app.services.technical_debt_service import TechnicalDebtService
from app.services.bottleneck_service import BottleneckService

router = APIRouter()


@router.get("/team/{team_id}/effectiveness", response_model=TeamEffectivenessMetrics)
def get_team_effectiveness(
    team_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    project_id: int = Query(default=None, description="Optional project ID to filter metrics"),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive team effectiveness metrics including:
    - Overall effectiveness score (0-100)
    - Activity metrics (commits, PRs, active contributors)
    - Performance indicators
    - Alerts and recommendations
    - Optional project_id filter to analyze specific project
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    metrics = TeamEffectivenessService.calculate_effectiveness_score(
        db, team_id, period_start, period_end, project_id=project_id
    )
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Save metric to database
    TeamEffectivenessService.save_team_metric(
        db=db,
        team_id=team_id,
        metric_type="effectiveness_score",
        metric_data=metrics,
        score=metrics["effectiveness_score"],
        trend=metrics["trend"],
        period_start=period_start,
        period_end=period_end,
        has_alert=metrics["has_alert"],
        alert_message=metrics["alert_message"],
        alert_severity=metrics["alert_severity"]
    )
    
    return metrics


@router.get("/team/{team_id}/technical-debt", response_model=TechnicalDebtAnalysis)
def get_technical_debt_analysis(
    team_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    project_id: int = Query(default=None, description="Optional project ID to filter metrics"),
    db: Session = Depends(get_db)
):
    """
    Analyze technical debt trends including:
    - Test coverage trends
    - TODO comment growth
    - Code review quality metrics
    - Recommendations for improvement
    - Optional project_id filter to analyze specific project
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    analysis = TechnicalDebtService.analyze_technical_debt(
        db=db,
        team_id=team_id,
        project_id=project_id,
        period_start=period_start,
        period_end=period_end
    )
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Save metric
    TechnicalDebtService.save_technical_debt_metric(
        db=db,
        team_id=team_id,
        metrics=analysis,
        period_start=period_start,
        period_end=period_end
    )
    
    return analysis


@router.get("/team/{team_id}/bottlenecks", response_model=BottleneckAnalysis)
def get_bottleneck_analysis(
    team_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    project_id: int = Query(default=None, description="Optional project ID to filter metrics"),
    db: Session = Depends(get_db)
):
    """
    Analyze workflow bottlenecks including:
    - Time spent in each stage (todo, development, review, testing)
    - Identification of slowest stage
    - Impact assessment
    - Recommendations to improve workflow
    - Optional project_id filter to analyze specific project
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    analysis = BottleneckService.analyze_bottlenecks(
        db=db,
        team_id=team_id,
        project_id=project_id,
        period_start=period_start,
        period_end=period_end
    )
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return analysis


@router.get("/project/{project_id}/technical-debt", response_model=TechnicalDebtAnalysis)
def get_project_technical_debt(
    project_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get technical debt analysis for a specific project."""
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    analysis = TechnicalDebtService.analyze_technical_debt(
        db=db,
        project_id=project_id,
        period_start=period_start,
        period_end=period_end
    )
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return analysis

