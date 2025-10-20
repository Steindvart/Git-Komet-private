# Git-Komet Backend

Backend API for the Git-Komet team effectiveness analysis system.

## Tech Stack

- **Python 3.10+**
- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database
- **GitPython** - Git repository interaction

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy environment file:
```bash
cp .env.example .env
```

4. Initialize database:
```bash
python init_db.py
```

5. Run the server:
```bash
python run.py
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Repositories
- `GET /api/v1/repositories` - List all repositories
- `POST /api/v1/repositories` - Create a new repository
- `GET /api/v1/repositories/{id}` - Get repository details
- `PUT /api/v1/repositories/{id}` - Update repository
- `DELETE /api/v1/repositories/{id}` - Delete repository
- `POST /api/v1/repositories/{id}/sync` - Sync repository commits from Git

### Teams
- `GET /api/v1/teams` - List all teams
- `POST /api/v1/teams` - Create a new team
- `GET /api/v1/teams/{id}` - Get team details
- `DELETE /api/v1/teams/{id}` - Delete team
- `POST /api/v1/teams/members` - Add team member
- `GET /api/v1/teams/{id}/members` - Get team members
- `DELETE /api/v1/teams/members/{id}` - Remove team member

### Metrics
- `GET /api/v1/metrics/team/{id}/effectiveness` - Get team effectiveness metrics
- `GET /api/v1/metrics/repository/{id}` - Get repository metrics
- `POST /api/v1/metrics/repository/{id}/calculate` - Calculate and save metrics

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── endpoints/      # API route handlers
│   ├── core/               # Core configuration
│   ├── db/                 # Database configuration
│   ├── models/             # SQLAlchemy models
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   └── main.py            # FastAPI application
├── tests/                  # Tests
├── .env.example           # Environment variables example
├── requirements.txt       # Python dependencies
├── init_db.py            # Database initialization script
└── run.py                # Application runner
```

## Development

Run with auto-reload:
```bash
python run.py
```

Or use uvicorn directly:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
