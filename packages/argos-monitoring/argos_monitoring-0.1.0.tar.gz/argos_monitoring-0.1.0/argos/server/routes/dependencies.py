from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

auth_scheme = HTTPBearer()


def get_db(request: Request):
    db = request.app.state.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_config(request: Request):
    return request.app.state.config


async def verify_token(
    request: Request, token: HTTPAuthorizationCredentials = Depends(auth_scheme)
):
    """Verify agent token"""
    if token.credentials not in request.app.state.config.service.secrets:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token
