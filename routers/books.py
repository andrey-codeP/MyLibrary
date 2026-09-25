from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated

from schemas.book import SBookAdd, SBook
from database.depends import SessionDep
from repository.books import BooksRepository
from security import VerifTokenAndGetId

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)


@router.post("", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: SBookAdd, session: SessionDep, current_user_id: VerifTokenAndGetId
):
    book_model = await BooksRepository.add_book(book, current_user_id, session)
    return book_model


@router.get("/{book_id}", response_model=SBook, status_code=status.HTTP_200_OK)
async def get_book(
    book_id: int, session: SessionDep, current_user_id: VerifTokenAndGetId
):
    book = await BooksRepository.get_book(book_id, current_user_id, session)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return book


@router.get("", response_model=list[SBook], status_code=status.HTTP_200_OK)
async def get_books(session: SessionDep, current_user_id: VerifTokenAndGetId):
    books = await BooksRepository.get_all_books(current_user_id, session)
    return books


@router.put("/{book_id}", response_model=SBook, status_code=status.HTTP_200_OK)
async def update_book(
    book_id: int,
    book: SBookAdd,
    session: SessionDep,
    current_user_id: VerifTokenAndGetId,
):
    update_model = await BooksRepository.update_book(
        current_user_id, book, book_id, session
    )
    if update_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return update_model


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int, session: SessionDep, current_user_id: VerifTokenAndGetId
):
    delete_model = await BooksRepository.delete_book(current_user_id, book_id, session)
    if delete_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return None
