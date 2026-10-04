from app.security import (
    verify_password_or_hash,
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
)
from fastapi import APIRouter, Depends, HTTPException, status, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime, timedelta, timezone

from app.config import settings
from app.repository.authrep import AuthUserRepository
from app.repository.tokens import TokenRepository

from app.schemas.user import UserInDb
from app.database.depends import SessionDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def authorization_user(user: UserInDb, session: SessionDep):
    craeted_user = await AuthUserRepository.create_user(user, session)
    return craeted_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    user_in_db = await AuthUserRepository.get_user_by_username(
        user_data.username, session
    )

    if user_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    user_id, hashed_password = user_in_db.id, user_in_db.hashed_password

    if not verify_password_or_hash(user_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    access_token: str = create_access_token(user_id)

    refresh_token: str = create_refresh_token(user_id)
    refresh_token_hash = hash_refresh_token(refresh_token)
    refresh_expired_at = datetime.now(timezone.utc) + timedelta(
        days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
    )

    await TokenRepository.create_token(
        user_id=user_id,
        hashed_token=refresh_token_hash,
        expires_at=refresh_expired_at,
        session=session,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def get_new_access_token(
    response: Response,
    session: SessionDep,
    token: Annotated[str | None, Cookie(alias="refresh_token")] = None
):

    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is missing",
        )
    hashed_token = hash_refresh_token(token)
    token_in_db = await TokenRepository.get_by_hashed_token(hashed_token, session)

    if token_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is invalid",
        )

    now = datetime.now(timezone.utc)

    if token_in_db.expires_at <= now:
        await TokenRepository.delete_by_hashed_token(token_in_db.hashed_token, session)

        response.delete_cookie(
            key="refresh_token",
            path="/",
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is expired",
        )

    user = token_in_db.user

    access_token = create_access_token(user.id)

    new_refresh_token = create_refresh_token(user.id)
    new_refresh_token_hash = hash_refresh_token(new_refresh_token)

    await TokenRepository.rotate(
        token=token_in_db,
        new_hashed_token=new_refresh_token_hash,
        new_expires_at=now + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
        session=session,
    )

    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=False,  # Только localhost / HTTP. В production: True.
        samesite="lax",
        max_age=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/",
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
