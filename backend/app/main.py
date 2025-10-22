from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import init_db
from app.api import projects, pull_requests, issues, metrics, mock

# Инициализация FastAPI приложения
app = FastAPI(
    title="Git Komet API",
    description="API для анализа эффективности команд через Git-метрики",
    version="1.0.0"
)

# Настройка CORS для доступа с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(projects.router)
app.include_router(pull_requests.router)
app.include_router(issues.router)
app.include_router(metrics.router)
app.include_router(mock.router)


@app.on_event("startup")
def on_startup():
    """Инициализация БД при запуске"""
    init_db()


@app.get("/")
def root():
    """Корневой endpoint"""
    return {
        "message": "Welcome to Git Komet API",
        "version": "1.0.0",
        "description": "Система автооценки эффективности команд через анализ Git-метрик",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy"}
