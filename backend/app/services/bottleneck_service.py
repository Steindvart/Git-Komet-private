from typing import Dict, List
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import Team, TeamMember, Task, PullRequest


class BottleneckService:
    """Service for analyzing workflow bottlenecks."""

    @staticmethod
    def analyze_bottlenecks(
        db: Session,
        team_id: int,
        period_start: datetime,
        period_end: datetime
    ) -> Dict:
        """Analyze workflow bottlenecks by stage."""
        team = db.query(Team).filter(Team.id == team_id).first()
        if not team:
            return None
        
        member_ids = [m.id for m in team.members]
        
        # Get tasks for the team
        tasks = db.query(Task).filter(
            Task.assignee_id.in_(member_ids),
            Task.created_at.between(period_start, period_end)
        ).all()
        
        # Get pull requests
        prs = db.query(PullRequest).filter(
            PullRequest.author_id.in_(member_ids),
            PullRequest.created_at.between(period_start, period_end)
        ).all()
        
        if not tasks and not prs:
            return {
                "team_id": team_id,
                "bottleneck_stage": "none",
                "avg_time_in_stage": 0,
                "affected_tasks_count": 0,
                "impact_score": 0,
                "recommendations": ["No data available for the period"],
                "period_start": period_start,
                "period_end": period_end,
            }
        
        # Calculate average time in each stage
        stages = {
            "todo": [],
            "development": [],
            "review": [],
            "testing": []
        }
        
        for task in tasks:
            if task.time_in_todo:
                stages["todo"].append(task.time_in_todo)
            if task.time_in_development:
                stages["development"].append(task.time_in_development)
            if task.time_in_review:
                stages["review"].append(task.time_in_review)
            if task.time_in_testing:
                stages["testing"].append(task.time_in_testing)
        
        # Add PR review times to review stage
        for pr in prs:
            if pr.time_to_first_review:
                stages["review"].append(pr.time_to_first_review)
        
        # Calculate averages
        stage_averages = {}
        for stage, times in stages.items():
            if times:
                stage_averages[stage] = sum(times) / len(times)
            else:
                stage_averages[stage] = 0
        
        # Find bottleneck (stage with highest average time)
        if stage_averages:
            bottleneck_stage = max(stage_averages, key=stage_averages.get)
            avg_time_in_stage = stage_averages[bottleneck_stage]
        else:
            bottleneck_stage = "none"
            avg_time_in_stage = 0
        
        # Count affected tasks
        affected_tasks_count = len(stages.get(bottleneck_stage, []))
        
        # Calculate impact score (0-100, higher means more severe bottleneck)
        if avg_time_in_stage == 0:
            impact_score = 0
        else:
            # Impact based on time and number of affected items
            time_impact = min(100, (avg_time_in_stage / 24) * 20)  # Per day
            volume_impact = min(50, affected_tasks_count * 5)
            impact_score = time_impact + volume_impact
        
        # Generate recommendations
        recommendations = []
        
        if bottleneck_stage == "review":
            recommendations.append(
                f"⚠️ Code review is a bottleneck (avg {avg_time_in_stage:.1f} hours). "
                "Consider: increasing reviewer capacity, setting review SLAs, or implementing automated checks."
            )
            if avg_time_in_stage > 48:
                recommendations.append(
                    "Reviews are taking over 2 days on average. "
                    "Ensure team members are notified of pending reviews and prioritize review tasks."
                )
        elif bottleneck_stage == "development":
            recommendations.append(
                f"⚠️ Development stage is taking long (avg {avg_time_in_stage:.1f} hours). "
                "Consider: breaking down tasks, pair programming, or addressing technical debt."
            )
        elif bottleneck_stage == "testing":
            recommendations.append(
                f"⚠️ Testing is a bottleneck (avg {avg_time_in_stage:.1f} hours). "
                "Consider: increasing test automation, parallel testing, or adding QA resources."
            )
        elif bottleneck_stage == "todo":
            recommendations.append(
                f"Tasks are waiting to be started (avg {avg_time_in_stage:.1f} hours). "
                "Review backlog prioritization and team capacity."
            )
        
        if impact_score > 70:
            recommendations.append(
                "🚨 High impact bottleneck detected. Immediate action recommended to improve workflow."
            )
        elif impact_score > 40:
            recommendations.append(
                "⚠️ Moderate bottleneck detected. Consider process improvements."
            )
        
        if not recommendations:
            recommendations.append("No significant bottlenecks detected. Workflow is running smoothly.")
        
        # Add stage-specific metrics
        stage_breakdown = {
            stage: {
                "avg_time": round(avg, 2),
                "count": len(stages[stage])
            }
            for stage, avg in stage_averages.items()
        }
        
        return {
            "team_id": team_id,
            "bottleneck_stage": bottleneck_stage,
            "avg_time_in_stage": round(avg_time_in_stage, 2),
            "affected_tasks_count": affected_tasks_count,
            "impact_score": round(impact_score, 2),
            "recommendations": recommendations,
            "stage_breakdown": stage_breakdown,
            "period_start": period_start,
            "period_end": period_end,
        }
