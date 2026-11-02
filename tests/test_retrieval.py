# 测试 AzureSearchRetriever:用 fake client,不碰真实 Azure
from types import SimpleNamespace

from app.services.retrieval import AzureSearchRetriever


class FakeOpenAI:
    def __init__(self) -> None:
        self.embedding_calls: list[dict] = []
        self.embeddings = SimpleNamespace(create=self._create)

    def _create(self, **kwargs) -> SimpleNamespace:
        self.embedding_calls.append(kwargs)
        return SimpleNamespace(data=[SimpleNamespace(embedding=[0.1, 0.2, 0.3])])


class FakeSearchClient:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def search(self, **kwargs) -> list[dict]:
        self.calls.append(kwargs)
        return [{"id": "doc-0", "content": "some text", "@search.score": 0.5}]


def test_retriever_does_hybrid_search_and_maps_results() -> None:
    search = FakeSearchClient()
    openai = FakeOpenAI()
    retriever = AzureSearchRetriever(search, openai, "embedding")  # type: ignore[arg-type]

    sources = retriever.search("what is x?")

    assert openai.embedding_calls[0]["model"] == "embedding"
    assert search.calls[0]["search_text"] == "what is x?"  # keyword 部分
    assert len(search.calls[0]["vector_queries"]) == 1  # vector 部分
    assert sources[0].doc_id == "doc-0"
    assert sources[0].text == "some text"
    assert sources[0].score == 0.5