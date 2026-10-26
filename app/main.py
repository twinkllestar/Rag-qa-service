# 应用入口:创建 FastAPI instance,并把各个 router 挂上去
from fastapi import FastAPI

from app.api import ask, health

app = FastAPI(title="RAG QA Service")
app.include_router(health.router)
app.include_router(ask.router)