from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.database_models import Base

# SQLite database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./git_komet.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Инициализация базы данных"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Получение сессии БД для dependency injection"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
