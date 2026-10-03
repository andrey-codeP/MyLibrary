import pytest
from pydantic import ValidationError
from app.schemas.user import UserInDb


@pytest.mark.parametrize(
    "noncorrect_username, noncorrect_password",
    [("си", "сев"), ("сикс", "сев"), ("сикс", "а" * 21), ("с" * 21, "севееен")],
)
async def test_user_in_db_schemas(noncorrect_username, noncorrect_password):
    with pytest.raises(ValidationError):
        UserInDb(username=noncorrect_username, password=noncorrect_password)
