import pytest
from pydantic import ValidationError
from app.schemas.book import SBookAdd


@pytest.mark.parametrize("page", [3, -1, 0])
async def test_book_add_scheams(page: int):
    with pytest.raises(ValidationError) as excinfo:
        SBookAdd(title="...", author="...", year=10, pages=page)
