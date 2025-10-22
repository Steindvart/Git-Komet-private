from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import metrics, repositories

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Git-Komet: Project effectiveness analysis through Git metrics"
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


@app.get("/")
async def root():
    return {
        "message": "Git-Komet API",
        "description": "Project effectiveness analysis through Git metrics",
        "version": "2.0.0",
        "features": [
            "Project effectiveness scoring",
            "Technical debt analysis",
            "Bottleneck detection",
            "Employee care metrics",
            "Trend analysis and alerts"
        ]
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
