from pwdlib import PasswordHash


pwd_context = PasswordHash.recommended()


def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password_or_hash(
    plain_password_or_hash: str, hashed_password_or_hash: str
) -> bool:
    return pwd_context.verify(
        plain_password_or_hash, hashed_password_or_hash
    )  # знаю что плохой вариант с такой функцией, но для учебного проекта думаю ок


import hashlib


def hash_refresh_token(refresh_token: str) -> str:
    return hashlib.sha256(
        refresh_token.encode("utf-8")
    ).hexdigest()