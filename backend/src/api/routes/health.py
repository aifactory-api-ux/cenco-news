from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/health")
async def health_check():
    return JSONResponse({"status": "ok", "service": "cenco-news-backend", "version": "1.0.0"})


@router.get("/health/ready")
async def readiness_check():
    # Implement readiness checks here, e.g. DB connection
    return JSONResponse({"status": "ready"})
