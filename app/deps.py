from fastapi import Request

from app.services.matter_client import MatterClient


def get_matter_client(request: Request) -> MatterClient:
    return request.app.state.matter_client
