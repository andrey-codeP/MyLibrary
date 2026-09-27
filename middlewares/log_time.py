from fastapi import Request
import time

from logger import logger as logger_for_time


async def log_and_time_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    logger_for_time.info(f"---> [начался запрос] {request.method} {request.url.path}")

    response = await call_next(request)

    end_time = (time.perf_counter() - start_time) * 1000
    logger_for_time.info(
        f"<--- завершен запрос: {request.method} {request.url.path} "
        f"статус: {response.status_code} | за время {end_time:.2f}ms"
    )

    return response
