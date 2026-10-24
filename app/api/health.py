# 健康检查接口:部署后平台会用它判断服务是否活着
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}