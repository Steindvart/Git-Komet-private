from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.models import Team as TeamModel, TeamMember as TeamMemberModel
from app.schemas.schemas import Team, TeamCreate, TeamMember, TeamMemberCreate

router = APIRouter()


@router.get("/", response_model=List[Team])
def list_teams(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all teams."""
    teams = db.query(TeamModel).offset(skip).limit(limit).all()
    return teams


@router.post("/", response_model=Team)
def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db)
):
    """Create a new team."""
    # Check if team already exists
    existing = db.query(TeamModel).filter(TeamModel.name == team.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Team already exists")
    
    db_team = TeamModel(**team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


@router.get("/{team_id}", response_model=Team)
def get_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific team."""
    team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


@router.delete("/{team_id}")
def delete_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    """Delete a team."""
    team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    db.delete(team)
    db.commit()
    return {"message": "Team deleted successfully"}


@router.post("/members", response_model=TeamMember)
def add_team_member(
    member: TeamMemberCreate,
    db: Session = Depends(get_db)
):
    """Add a member to a team."""
    # Check if team exists
    team = db.query(TeamModel).filter(TeamModel.id == member.team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if member already exists in team
    existing = db.query(TeamMemberModel).filter(
        TeamMemberModel.team_id == member.team_id,
        TeamMemberModel.email == member.email
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Member already in team")
    
    db_member = TeamMemberModel(**member.dict())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.get("/{team_id}/members", response_model=List[TeamMember])
def get_team_members(
    team_id: int,
    db: Session = Depends(get_db)
):
    """Get all members of a team."""
    team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return team.members


@router.delete("/members/{member_id}")
def remove_team_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    """Remove a member from a team."""
    member = db.query(TeamMemberModel).filter(TeamMemberModel.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    db.delete(member)
    db.commit()
    return {"message": "Member removed successfully"}
