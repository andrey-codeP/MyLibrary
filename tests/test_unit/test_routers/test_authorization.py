import pytest
from fastapi import status
from datetime import datetime, timezone, timedelta

from app.database.models.user import UserTable
from app.database.models.tokens import Tokens
from app.security import get_hash_password, hash_refresh_token



@pytest.mark.asyncio
async def test_authorization_post(user_dict_test, user_clients):
    response = await user_clients.post("/auth/register", json=user_dict_test)
    assert response.status_code == status.HTTP_201_CREATED

    response_data = response.json()

    assert response_data["username"] == "тестовый_раб"


@pytest.mark.asyncio
async def test_login_post(user_dict_test, client, get_db_sess):
    plain_password = user_dict_test["password"]
    user = UserTable(
        username=user_dict_test["username"],
        hashed_password=get_hash_password(plain_password),
    )
    get_db_sess.add(user)
    await get_db_sess.commit()

    login_payload = {"username": user_dict_test["username"], "password": plain_password}

    response = await client.post("/auth/login", data=login_payload)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"

    assert response.cookies.get("refresh_token") is not None


@pytest.mark.asyncio
async def test_login_lost_user_not_in_db(client):
    login_payload = {"username": "гость6767", "password": "нетиди"}
    response = await client.post("/auth/login", data=login_payload)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_login_wrong_password(client, get_db_sess):
    user_in_db = UserTable(
        username="гость1488", hashed_password=get_hash_password("нетупар")
    )

    get_db_sess.add(user_in_db)
    await get_db_sess.commit()
    login_payload = {"username": "гость1488", "password": "неправильно"}

    response = await client.post("/auth/login", data=login_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_new_tokens(client, get_db_sess):

    user = UserTable(
        username="гость228",
        hashed_password=get_hash_password("пароль")
    )
    get_db_sess.add(user)
    await get_db_sess.flush()

    refresh = "valid_refresh_token"
    hashed_refresh = hash_refresh_token(refresh)

    token_in_db = Tokens(
        user_id=user.id,
        hashed_token=hashed_refresh,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )

    get_db_sess.add(token_in_db)
    await get_db_sess.commit()

    client.cookies.set("refresh_token", refresh)
    response = await client.post("/auth/refresh")

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()
    assert "refresh_token" in response.cookies


@pytest.mark.asyncio
async def test_no_token(client, get_db_sess):

    client.cookies.clear()
    response = await client.post("/auth/refresh")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_tokens_error_db(client, get_db_sess):

    client.cookies.set("refresh_token", "fake_token")
    response = await client.post("/auth/refresh")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_expire_token(client, get_db_sess):
    user = UserTable(
        username="гость228",
        hashed_password=get_hash_password("пароль")
    )
    get_db_sess.add(user)
    await get_db_sess.flush()

    refresh = "valid_refresh_token"
    hashed_refresh = hash_refresh_token(refresh)

    token_in_db = Tokens(
        user_id=user.id,
        hashed_token=hashed_refresh,
        expires_at=datetime.now(timezone.utc) - timedelta(hours=2)
    )
    get_db_sess.add(token_in_db)
    await get_db_sess.commit()

    client.cookies.set("refresh_token", refresh)

    response = await client.post("/auth/refresh")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "refresh_token" not in response.cookies