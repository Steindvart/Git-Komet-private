from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.db.session import get_db
from app.schemas.schemas import (
    ProjectEffectivenessMetrics,
    EmployeeCareMetrics,
    ActiveContributorsMetrics,
    CommitsPerPersonMetrics,
    TechnicalDebtAnalysis,
    BottleneckAnalysis,
    PRsNeedingAttentionResponse
)
from app.services.project_effectiveness_service import ProjectEffectivenessService
from app.services.project_technical_debt_service import ProjectTechnicalDebtService
from app.services.project_bottleneck_service import ProjectBottleneckService

router = APIRouter()


@router.get("/project/{project_id}/technical-debt", response_model=TechnicalDebtAnalysis)
def get_project_technical_debt(
    project_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Получить анализ технического долга для проекта.
    Get technical debt analysis for a specific project.
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    analysis = ProjectTechnicalDebtService.analyze_technical_debt(
        db=db,
        project_id=project_id,
        period_start=period_start,
        period_end=period_end
    )
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Сохранить метрику
    ProjectTechnicalDebtService.save_technical_debt_metric(
        db=db,
        project_id=project_id,
        metrics=analysis,
        period_start=period_start,
        period_end=period_end
    )
    
    return analysis


@router.get("/project/{project_id}/effectiveness", response_model=ProjectEffectivenessMetrics)
def get_project_effectiveness(
    project_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Получить комплексные метрики эффективности проекта.
    Get comprehensive project effectiveness metrics including:
    - Overall effectiveness score (0-100)
    - Activity metrics (commits, PRs, active contributors)
    - Performance indicators
    - Work-life balance metrics
    - Alerts and recommendations
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    metrics = ProjectEffectivenessService.calculate_effectiveness_score(
        db, project_id, period_start, period_end
    )
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Сохранить метрику
    ProjectEffectivenessService.save_project_metric(
        db=db,
        project_id=project_id,
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


@router.get("/project/{project_id}/employee-care", response_model=EmployeeCareMetrics)
def get_project_employee_care(
    project_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Получить агрегированную метрику заботы о сотрудниках для проекта.
    Get aggregated employee care metric for the project.
    
    Эта метрика отслеживает work-life balance на уровне проекта:
    - Процент коммитов после рабочего времени
    - Процент коммитов в выходные дни
    - Общую оценку заботы о сотрудниках (0-100)
    - Статус (excellent, good, needs_attention, critical)
    - Рекомендации по улучшению
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    metrics = ProjectEffectivenessService.calculate_employee_care_metric(
        db, project_id, period_start, period_end
    )
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Сохранить метрику
    ProjectEffectivenessService.save_project_metric(
        db=db,
        project_id=project_id,
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


@router.get("/project/{project_id}/bottlenecks", response_model=BottleneckAnalysis)
def get_project_bottlenecks(
    project_id: int,
    period_days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """
    Анализ узких мест workflow проекта.
    Analyze workflow bottlenecks for a project including:
    - Time spent in each stage (todo, development, review, testing)
    - Identification of slowest stage
    - Impact assessment
    - Recommendations to improve workflow
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    analysis = ProjectBottleneckService.analyze_bottlenecks(
        db=db,
        project_id=project_id,
        period_start=period_start,
        period_end=period_end
    )
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return analysis


@router.get("/project/{project_id}/prs-needing-attention", response_model=PRsNeedingAttentionResponse)
def get_prs_needing_attention(
    project_id: int,
    min_hours: float = Query(default=0.0, ge=0, description="Минимальное количество часов на ревью (0 = все PR)"),
    limit: int = Query(default=5, ge=1, le=20, description="Максимальное количество PR для возврата"),
    db: Session = Depends(get_db)
):
    """
    Получить список PR/MR (запросов).
    Get list of PR/MRs (requests).
    
    Этот endpoint возвращает PR/MR, отсортированные по времени нахождения на ревью.
    По умолчанию возвращает все открытые PR/MR (min_hours=0).
    
    УСТАРЕЛО: В новом ТЗ у нас нет доступа к данным о PR/MR.
    """
    prs = ProjectBottleneckService.get_prs_needing_attention(
        db=db,
        project_id=project_id,
        min_hours_in_review=min_hours,
        limit=limit
    )
    
    if prs is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "project_id": project_id,
        "prs": prs,
        "total_count": len(prs)
    }


@router.get("/project/{project_id}/active-contributors", response_model=ActiveContributorsMetrics)
def get_active_contributors(
    project_id: int,
    period_days: int = Query(default=30, ge=1, le=365, description="Период анализа в днях (по умолчанию 30 дней)"),
    db: Session = Depends(get_db)
):
    """
    Получить метрику активных участников проекта.
    Get active contributors metric for the project.
    
    Новое ТЗ: Анализ активных участников - количество активных участников,
    чтобы понимать сколько примерно человеческих ресурсов тратится на проект по факту.
    Берутся все коммиты за последний месяц и смотрим кто автор.
    Каждый уникальный автор - это активный участник.
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    metrics = ProjectEffectivenessService.calculate_active_contributors(
        db, project_id, period_start, period_end
    )
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return metrics


@router.get("/project/{project_id}/commits-per-person", response_model=CommitsPerPersonMetrics)
def get_commits_per_person(
    project_id: int,
    period_days: int = Query(default=30, ge=1, le=365, description="Период анализа в днях (по умолчанию 30 дней)"),
    db: Session = Depends(get_db)
):
    """
    Получить количество коммитов на каждого участника проекта.
    Get commit count per person for the project.
    
    Новое ТЗ: Количество коммитов на того или иного человека,
    чтобы понимать уровень экспертности по проекту.
    Метрика включает:
    - Количество коммитов каждого участника
    - Количество измененных строк
    - Уровень экспертности (beginner, intermediate, advanced, expert)
    """
    period_end = datetime.utcnow()
    period_start = period_end - timedelta(days=period_days)
    
    metrics = ProjectEffectivenessService.calculate_commits_per_person(
        db, project_id, period_start, period_end
    )
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return metrics

