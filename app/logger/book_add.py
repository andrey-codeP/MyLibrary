import logging

log_format = logging.Formatter(
    "%(asctime)s - %(filename)s - %(levelname)s - %(message)s"
)

books_logger = logging.getLogger("books_audit")
books_logger.setLevel(logging.INFO)
books_logger.propagate = False

# Добавляем обработчики для книг
books_file = logging.FileHandler("book.log", encoding="UTF-8")
books_file.setFormatter(log_format)
books_logger.addHandler(books_file)
books_logger.addHandler(logging.StreamHandler())
