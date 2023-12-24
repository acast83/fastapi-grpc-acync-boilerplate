import uvicorn
from fastapi import FastAPI

from .health import router as health_router
from .activity_log.activity_log import router as activity_log_router
from .lookups.lookups import router as lookups_router
from .users.users import router as users_router

app = FastAPI(docs_url="/api/docs", redoc_url="/api/redocs", openapi_url="/api/openapi.json")
app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(activity_log_router, prefix="/activity-log", tags=["Activity Log"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(lookups_router, prefix="/lookups", tags=["Lookups"])

__all__ = ["app"]

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=9000)
