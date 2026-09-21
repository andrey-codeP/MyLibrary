from security import get_hash_password, verify_password
from fastapi import APIRouter, Depends, HTTPException, status
from database.depends import SessionDep

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def authorization_user():
    ...