import pytest

@pytest.fixture
def fake_book(mocker):
    book = mocker.MagicMock()
    book.title = "my_title"
    book.author = "my_author"
    book.year = "11"
    book.pages = 12
    return book

