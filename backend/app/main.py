from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.routers import analytics
from app.routers import auth
from app.routers import datasets
from app.routers import forecasts
from app.routers import health
from app.routers import jobs
from app.routers import reports
from app.routers import users

settings = get_settings()
configure_logging()

app = FastAPI(
  title=settings.app_name,
  version="0.1.0",
)


# Configure frontend CORS access.
app.add_middleware(
  CORSMiddleware,
  allow_origins=[settings.frontend_origin],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


# Return a root health message.
@app.get("/")
def read_root():
  return {
    "message": "AI Analytics Automation Platform API"
  }


app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(datasets.router, prefix="/api/datasets", tags=["datasets"])
app.include_router(jobs.router, prefix="/api/jobs", tags=["jobs"])
app.include_router(reports.router, prefix="/api/reports", tags=["reports"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(forecasts.router, prefix="/api/forecasts", tags=["forecasts"])