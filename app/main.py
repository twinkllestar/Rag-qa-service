# 应用入口:创建 FastAPI 实例,并把各个模块的路由挂上去
from fastapi import FastAPI

from app.api import health

app = FastAPI(title="RAG QA Service")
app.include_router(health.router)