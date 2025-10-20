from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import metrics, repositories, teams

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Git-Komet: Team effectiveness analysis through Git metrics"
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(repositories.router, prefix=f"{settings.API_V1_STR}/projects", tags=["projects"])
app.include_router(metrics.router, prefix=f"{settings.API_V1_STR}/metrics", tags=["metrics"])
app.include_router(teams.router, prefix=f"{settings.API_V1_STR}/teams", tags=["teams"])


@app.get("/")
async def root():
    return {
        "message": "Git-Komet API",
        "description": "Team effectiveness analysis through Git metrics",
        "version": "2.0.0",
        "features": [
            "Team effectiveness scoring",
            "Technical debt analysis",
            "Bottleneck detection",
            "Trend analysis and alerts"
        ]
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
