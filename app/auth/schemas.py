from pydantic import BaseModel


class GetAuthCodePayload(BaseModel):
    client_id: str
    client_secret: str
    hash: str


class GetAuthTokenPayload(BaseModel):
    code: str
    signature: str