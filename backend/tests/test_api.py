import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import Base, get_db

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(test_db):
    return TestClient(app)


def test_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Git-Komet API"


def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_repository(client):
    """Test creating a repository"""
    repo_data = {
        "name": "Test Repo",
        "url": "https://github.com/test/repo.git",
        "description": "Test repository"
    }
    response = client.post("/api/v1/repositories", json=repo_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == repo_data["name"]
    assert data["url"] == repo_data["url"]
    assert "id" in data


def test_list_repositories(client):
    """Test listing repositories"""
    response = client.get("/api/v1/repositories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_team(client):
    """Test creating a team"""
    team_data = {
        "name": "Test Team",
        "description": "A test team"
    }
    response = client.post("/api/v1/teams", json=team_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == team_data["name"]
    assert "id" in data


def test_list_teams(client):
    """Test listing teams"""
    response = client.get("/api/v1/teams")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
