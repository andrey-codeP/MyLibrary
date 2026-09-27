import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("ms.log", encoding="UTF-8"), logging.StreamHandler()],
)

logger = logging.getLogger()
