from database.models.user_table import UserTable
from database.models.book_table import Books  # <-- Убедитесь, что здесь импортируется Books, а не BookBase!

__all__ = ["UserTable", "Books"]