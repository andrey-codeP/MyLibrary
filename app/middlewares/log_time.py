from fastapi import Request
import time

from app.logger import ms_logger


async def log_and_time_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    ms_logger.info(f"---> [начался запрос] {request.method} {request.url.path}")

    response = await call_next(request)

    end_time = (time.perf_counter() - start_time) * 1000
    ms_logger.info(
        f"<--- завершен запрос: {request.method} {request.url.path} "
        f"статус: {response.status_code} | за время {end_time:.2f}ms"
    )

    return response
