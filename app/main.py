# 应用入口:创建 FastAPI instance,挂上 middleware 和各个 router
import logging
import time
import uuid

from fastapi import FastAPI, Request

from app.api import ask, health

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
logger = logging.getLogger("app.request")

app = FastAPI(title="RAG QA Service")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    # Middleware:每个 request 进来和出去都会经过这里
    request_id = uuid.uuid4().hex[:8]
    request.state.request_id = request_id
    start = time.perf_counter()

    response = await call_next(request)

    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "request_id=%s method=%s path=%s status=%d duration_ms=%.0f",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    response.headers["X-Request-ID"] = request_id  # 方便客户端报 bug 时带上这个 id
    return response


app.include_router(health.router)
app.include_router(ask.router)
logging.getLogger("azure").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpx2").setLevel(logging.WARNING)