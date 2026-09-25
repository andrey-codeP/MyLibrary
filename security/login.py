from fastapi import HTTPException, status, Depends, Cookie
from fastapi.security import OAuth2PasswordBearer

import jwt

from typing import Annotated
from datetime import datetime, timedelta, timezone


from config import settings

SECRET_KEY = settings.JWT_SECRET_TOKEN
JWT_ALGORITHM = "HS256"
oauth2_schemas = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(user_id: int) -> str:

    payload = {"sub": str(user_id), "type": "access"}

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    payload.update({"exp": int(expire.timestamp())})

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt


def create_refresh_token(user_id: int) -> str:

    payload = {"sub": str(user_id), "type": "refresh"}

    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )
    payload.update({"exp": int(expire.timestamp())})

    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def get_current_user_id(token: Annotated[str, Depends(oauth2_schemas)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])

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
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="the token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_user_id_from_refresh_token(
    refresh_token: Annotated[str | None, Cookie(default=None, alias="refresh_token")],
):
    try:
        if refresh_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token is missing",
            )

        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
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
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="the token is invalid",
            headers={"WWW-Authenticate": "Bearer"},
        )


VerifTokenAndGetId = Annotated[int, Depends(get_current_user_id)]
VerifyRefreshTokenAndGetId = Annotated[int, Depends(get_user_id_from_refresh_token)]
