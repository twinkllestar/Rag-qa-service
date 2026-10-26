# Retriever:根据 question 找出相关的文档片段 (chunks)
from typing import Protocol

from app.schemas.ask import Source


class Retriever(Protocol):
    # Protocol = contract。任何有 search() 的 class 都能当 Retriever 用
    def search(self, question: str) -> list[Source]: ...


class FakeRetriever:
    # 假的版本:return 写死的数据,用于development和 test
    def search(self, question: str) -> list[Source]:
        return [
            Source(
                doc_id="doc-1",
                text="FastAPI is a Python web framework for building APIs.",
                score=0.9,
            )
        ]