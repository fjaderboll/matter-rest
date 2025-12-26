from fastapi import APIRouter, Depends

from app.core.config import get_settings, Settings

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    return {"status": "ok", "app": settings.app_name}
