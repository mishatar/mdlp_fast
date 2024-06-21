# Python
import json
import httpx
from fastapi import FastAPI, Request, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# App
from const import API_URL
from utils.auth import ClosedResource  # Assuming it's a dependency for auth

app = FastAPI()

class GetAuthCodePayload(BaseModel):
    client_id: str
    client_secret: str
    hash: str

class GetAuthTokenPayload(BaseModel):
    code: str
    signature: str

@app.post("/get_auth_code")
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

@app.post("/get_auth_token")
async def get_auth_token(payload: GetAuthTokenPayload):
    user_token = await get_auth_token_request(
        {'code': payload.code, 'signature': payload.signature}
    )

    if user_token.status_code != 200:
        raise HTTPException(status_code=user_token.status_code, detail=user_token.json())

    return JSONResponse(content=user_token.json(), status_code=user_token.status_code)

async def get_auth_token_request(payload):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"https://{API_URL}/token",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
    return response

@app.get("/logout")
async def logout(Authorization: str = Header(None)):
    if not Authorization:
        raise HTTPException(status_code=400, detail="Authorization header missing")

    res = await logout_request(Authorization)

    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=res.json())

    return JSONResponse(content={"message": "User logout."}, status_code=res.status_code)

async def logout_request(auth_token):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://{API_URL}/auth/logout",
            headers={"Authorization": auth_token}
        )
    return response


self.request_session: ClientSession = ClientSession(
            base_url=service_config.service_config.service_url.rsplit("/", 1)[0],
            headers={
                "soapaction": "sendDocument",
                "content-type": "text/xml; charset=utf-8"
            },
            connector=TCPConnector(verify_ssl=False)
        )
