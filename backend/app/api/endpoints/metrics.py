from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.session import get_db
from app.schemas.schemas import (
    ProjectEffectivenessMetrics,
    RepositoryEffectivenessMetrics,
    EmployeeCareMetrics,
    ActiveContributorsMetrics,
    CommitsPerPersonMetrics,
    TechnicalDebtAnalysis,
    BottleneckAnalysis,
    PRsNeedingAttentionResponse
)
from app.services.project_aggregated_service import ProjectAggregatedService
from app.services.repository_effectiveness_service import RepositoryEffectivenessService
from app.services.repository_technical_debt_service import RepositoryTechnicalDebtService
from app.services.repository_bottleneck_service import RepositoryBottleneckService

router = APIRouter()


# Project-level aggregated endpoints
@router.get("/project/{project_id}/effectiveness", response_model=ProjectEffectivenessMetrics)
def get_project_effectiveness(
    project_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Получить агрегированные метрики эффективности проекта.
    Get aggregated project effectiveness metrics from all repositories.
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    metrics = ProjectAggregatedService.calculate_project_metrics(
        db, project_id, period_start, period_end
    )
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Сохранить метрику
    ProjectAggregatedService.save_project_metric(
        db=db,
        project_id=project_id,
        metric_type="effectiveness_score",
        metric_data=metrics,
        score=metrics["avg_effectiveness_score"],
        trend=metrics["trend"],
        period_start=period_start,
        period_end=period_end,
        has_alert=metrics["has_alert"],
        alert_message=metrics["alert_message"],
        alert_severity=metrics["alert_severity"]
    )
    
    return metrics


# Repository-level endpoints
@router.get("/repository/{repository_id}/effectiveness", response_model=RepositoryEffectivenessMetrics)
def get_repository_effectiveness(
    repository_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Получить комплексные метрики эффективности репозитория.
    Get comprehensive repository effectiveness metrics.
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    metrics = RepositoryEffectivenessService.calculate_effectiveness_score(
        db, repository_id, period_start, period_end
    )
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Сохранить метрику
    RepositoryEffectivenessService.save_repository_metric(
        db=db,
        repository_id=repository_id,
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


@router.get("/repository/{repository_id}/technical-debt", response_model=TechnicalDebtAnalysis)
def get_repository_technical_debt(
    repository_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Получить анализ технического долга для репозитория.
    Get technical debt analysis for a specific repository.
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    analysis = RepositoryTechnicalDebtService.analyze_technical_debt(
        db=db,
        repository_id=repository_id,
        period_start=period_start,
        period_end=period_end
    )
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Сохранить метрику
    RepositoryTechnicalDebtService.save_technical_debt_metric(
        db=db,
        repository_id=repository_id,
        metrics=analysis,
        period_start=period_start,
        period_end=period_end
    )
    
    return analysis


@router.get("/repository/{repository_id}/employee-care", response_model=EmployeeCareMetrics)
def get_repository_employee_care(
    repository_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Получить метрику заботы о сотрудниках для репозитория.
    Get employee care metric for the repository.
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    metrics = RepositoryEffectivenessService.calculate_employee_care_metric(
        db, repository_id, period_start, period_end
    )
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    # Сохранить метрику
    RepositoryEffectivenessService.save_repository_metric(
        db=db,
        repository_id=repository_id,
        metric_type="employee_care",
        metric_data=metrics,
        score=metrics["employee_care_score"],
        trend="stable",
        period_start=period_start,
        period_end=period_end,
        has_alert=metrics["status"] in ["needs_attention", "critical"],
        alert_message=metrics["recommendations"][0] if metrics["recommendations"] else None,
        alert_severity="warning" if metrics["status"] == "needs_attention" else "critical" if metrics["status"] == "critical" else None
    )
    
    return metrics


@router.get("/repository/{repository_id}/bottlenecks", response_model=BottleneckAnalysis)
def get_repository_bottlenecks(
    repository_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Анализ узких мест workflow репозитория.
    Analyze workflow bottlenecks for a repository.
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    analysis = RepositoryBottleneckService.analyze_bottlenecks(
        db=db,
        repository_id=repository_id,
        period_start=period_start,
        period_end=period_end
    )
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    return analysis