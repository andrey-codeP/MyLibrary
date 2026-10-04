from urllib import response

import pytest
from fastapi import status
from app.database.models.book import Books
from app.schemas.book import SBook


@pytest.mark.asyncio
async def test_create_book(client, book_dict_test):
    response = await client.post("/books", json=book_dict_test)

    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    assert response_data["title"] == "моякнижка"
    assert response_data["owner_id"] == 67


@pytest.mark.asyncio
async def test_get_book_with_id(client, book_dict_test, get_db_sess):

    create_response = await client.post("/books", json=book_dict_test)
    assert create_response.status_code == status.HTTP_201_CREATED

    created_book = create_response.json()
    book_id = created_book["id"]

    response = await client.get(f"/books/{book_id}")

    assert response.status_code == status.HTTP_200_OK

    response_data = response.json()

    assert response_data["title"] == book_dict_test["title"]
    assert response_data["owner_id"] == 67
    assert response_data["id"] == book_id


@pytest.mark.asyncio
async def test_get_book_by_id_error(client):
    book_id = 9595959

    response = await client.get(f"/books/{book_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_update_book(client, book_dict_test):
    create_response = await client.post("/books", json=book_dict_test)
    assert create_response.status_code == status.HTTP_201_CREATED
    response_data = create_response.json()

    response = await client.put(f"/books/{response_data['id']}", json=response_data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_update_book_with_none(client, book_dict_test):
    create_response = await client.post("/books", json=book_dict_test)
    assert create_response.status_code == status.HTTP_201_CREATED
    response_data = create_response.json()

    response = await client.put(f"/books/{9999999}", json=response_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_book_with_id(client, book_dict_test):
    create_response = await client.post("/books", json=book_dict_test)
    assert create_response.status_code == status.HTTP_201_CREATED
    data_response = create_response.json()
    book_id = data_response["id"]

    response = await client.delete(f"/books/{book_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.asyncio
async def test_delete_book_with_id_error(client, book_dict_test):
    create_response = await client.post("books", json=book_dict_test)
    assert create_response.status_code == status.HTTP_201_CREATED
    data_response = create_response.json()

    response = await client.delete(f"/books/67676767")
    assert response.status_code == status.HTTP_404_NOT_FOUND
