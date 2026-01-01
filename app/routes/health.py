from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.core.config import get_settings, Settings
from app.deps import get_matter_client
from app.services.matter_client import MatterClient

router = APIRouter(tags=["health"])


@router.get("/health")
async def health(
    settings: Settings = Depends(get_settings),
    client: MatterClient = Depends(get_matter_client),
):
    status = {
        "status": "ok",
        "app": settings.app_name
    }
    try:
        await client.health_check()
        return status
    except Exception as exc:
        status['status'] = "error"
        status['detail'] = str(exc)

        return JSONResponse(
            status_code=503,
            content=status,
        )
