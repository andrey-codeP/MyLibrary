from app.logger import book_add_logger
def background_log(book_title, user_id):
    book_add_logger.info(f"---> пользователь с айди: {user_id} создал книгу: {book_title}")
