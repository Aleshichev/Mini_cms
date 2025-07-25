from fastapi import FastAPI, Request, Response
from typing import Callable, Awaitable
import logging
import time

log = logging.getLogger(__name__)


async def add_process_time_to_requests(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.5f} seconds"
    return response


def register_middlewares(main_app: FastAPI) -> None:
    @main_app.middleware("http")
    async def log_new_request(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        log.info("Request %s to %s", request.method, request.url)
        return await call_next(request)
   
    main_app.middleware("http")(add_process_time_to_requests)