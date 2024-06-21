import httpx
from fastapi import Depends, status, APIRouter, Path, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.responses import JSONResponse

from app.auth.schemas import GetAuthCodePayload
from database import Connection

router = APIRouter(
    prefix='/auth',
    tags=['Auth'],
    include_in_schema=True
)

@router.post("/get_auth_code")
async def get_auth_code(payload: GetAuthCodePayload):
    payload_dict = {
        'client_id': payload.client_id,
        'client_secret': payload.client_secret,
        'user_id': payload.hash,
        'auth_type': "SIGNED_CODE"
    }
    user_code = await get_auth_code_request(payload_dict)

    if user_code.status_code != 200:
        raise HTTPException(status_code=user_code.status_code, detail=user_code.json())

    return JSONResponse(content=user_code.json(), status_code=user_code.status_code)


async def get_auth_code_request(payload):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://{API_URL}/auth",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
    return response
