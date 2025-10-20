from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Git-Komet"
    DEBUG: bool = True
    
    DATABASE_URL: str = "sqlite:///./git_komet.db"
    
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    DEFAULT_BRANCH: str = "main"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
