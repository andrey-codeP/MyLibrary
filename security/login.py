from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import jwt
from pwdlib import PasswordHash

from typing import Annotated
from datetime import datetime, timedelta, timezone


from config import settings

SECRET_KEY = settings.JWT_SECRET_TOKEN
ACCESS_TOKEN_ALGORITHM = "HS256"
oauth2_schemas = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(user_id: int) -> str:

    payload = {"sub": str(user_id), "type": "access"}

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload.update({"exp": int(expire.timestamp())})

    encoded_jwt = jwt.encode(
        payload, SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM
    )
    return encoded_jwt


def get_current_user_id(token: Annotated[str, Depends(oauth2_schemas)]):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM]
        )

        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="the token does not contain an ID",
            )

        return int(user_id)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="the token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="the token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )

VerifTokenAndGetId = Annotated[int, Depends(get_current_user_id)]
