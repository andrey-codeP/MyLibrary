from security import  verify_password, create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


from repository.authrep import AuthUserRepository
from schemas.user import UserInDb
from database.depends import SessionDep

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def authorization_user(user: UserInDb, session: SessionDep):
    craeted_user = await AuthUserRepository.create_user(user, session)
    return craeted_user


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    user_in_db = await AuthUserRepository.get_user_by_username(user_data.username, session)

    if user_in_db is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    user_id, hashed_password = user_in_db.id, user_in_db.hashed_password

    if not verify_password(user_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    token: str = create_access_token(user_id)
    return {"access_token": token, "token_type": "bearer"}
