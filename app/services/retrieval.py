# Retriever:根据 question 找出相关的文档片段 (chunks)
from typing import Protocol

from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import OpenAI

from app.schemas.ask import Source


class Retriever(Protocol):
    # Protocol = contract。任何有 search() 的 class 都能当 Retriever 用
    def search(self, question: str) -> list[Source]: ...


class FakeRetriever:
    # 假的版本:return 写死的数据,用于开发和 test
    def search(self, question: str) -> list[Source]:
        return [
            Source(
                doc_id="doc-1",
                text="FastAPI is a Python web framework for building APIs.",
                score=0.9,
            )
        ]


class AzureSearchRetriever:
    def __init__(
        self,
        search_client: SearchClient,
        openai_client: OpenAI,
        embedding_deployment: str,
        top_k: int = 3,
    ) -> None:
        # 两个 client 都从外面传进来 (dependency injection),方便 test 时换成 fake
        self._search = search_client
        self._openai = openai_client
        self._embedding_deployment = embedding_deployment
        self._top_k = top_k

    def search(self, question: str) -> list[Source]:
        # 1. 把 question 变成 vector
        embedding = (
            self._openai.embeddings.create(
                model=self._embedding_deployment, input=question
            )
            .data[0]
            .embedding
        )
        # 2. Hybrid search:search_text 做 keyword,vector_queries 做 vector,一次 query 完成
        vector_query = VectorizedQuery(
            vector=embedding, k_nearest_neighbors=self._top_k, fields="embedding"
        )
        results = self._search.search(
            search_text=question, vector_queries=[vector_query], top=self._top_k
        )
        return [
            Source(
                doc_id=r["id"], text=r["content"], score=float(r["@search.score"])
            )
            for r in results
        ]