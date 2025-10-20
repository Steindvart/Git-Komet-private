import git
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.models import Repository, Commit, TeamMember


class GitService:
    """Service for interacting with Git repositories and extracting metrics."""

    @staticmethod
    def clone_or_open_repository(repo_url: str, local_path: str) -> git.Repo:
        """Clone a repository or open existing one."""
        try:
            repo = git.Repo(local_path)
            repo.remotes.origin.pull()
            return repo
        except (git.exc.NoSuchPathError, git.exc.InvalidGitRepositoryError):
            return git.Repo.clone_from(repo_url, local_path)

    @staticmethod
    def extract_commits(repo: git.Repo, since: Optional[datetime] = None) -> List[dict]:
        """Extract commit information from a repository."""
        commits = []
        
        for commit in repo.iter_commits():
            if since and commit.committed_datetime < since:
                break
            
            stats = commit.stats.total
            commit_data = {
                "sha": commit.hexsha,
                "message": commit.message.strip(),
                "author_email": commit.author.email,
                "author_name": commit.author.name,
                "committed_at": commit.committed_datetime,
                "files_changed": stats.get("files", 0),
                "insertions": stats.get("insertions", 0),
                "deletions": stats.get("deletions", 0),
            }
            commits.append(commit_data)
        
        return commits

    @staticmethod
    def save_commits_to_db(
        db: Session, 
        repository_id: int, 
        commits_data: List[dict]
    ) -> int:
        """Save commits to database."""
        saved_count = 0
        
        for commit_data in commits_data:
            # Check if commit already exists
            existing = db.query(Commit).filter(
                Commit.sha == commit_data["sha"]
            ).first()
            
            if not existing:
                # Try to find team member by email
                author = db.query(TeamMember).filter(
                    TeamMember.email == commit_data["author_email"]
                ).first()
                
                commit = Commit(
                    repository_id=repository_id,
                    author_id=author.id if author else None,
                    **commit_data
                )
                db.add(commit)
                saved_count += 1
        
        db.commit()
        return saved_count
