# 测试 /ask:用 dependency_overrides 换成 test 专用的 fake,不碰任何外部服务
from fastapi.testclient import TestClient

from app.api.deps import get_llm, get_retriever
from app.main import app
from app.schemas.ask import Source


class EmptyRetriever:
    # 模拟 "什么都没检索到" 的情况
    def search(self, question: str) -> list[Source]:
        return []


client = TestClient(app)


def test_ask_returns_answer_and_sources() -> None:
    response = client.post("/ask", json={"question": "What is FastAPI?"})
    assert response.status_code == 200
    body = response.json()
    assert "answer" in body
    assert len(body["sources"]) == 1


def test_ask_rejects_empty_question() -> None:
    response = client.post("/ask", json={"question": ""})
    assert response.status_code == 422


def test_ask_rejects_missing_question() -> None:
    response = client.post("/ask", json={})
    assert response.status_code == 422


def test_ask_with_no_sources_says_dont_know() -> None:
    app.dependency_overrides[get_retriever] = lambda: EmptyRetriever()
    try:
        response = client.post("/ask", json={"question": "anything"})
        assert response.status_code == 200
        assert response.json()["sources"] == []
        assert "don't know" in response.json()["answer"]
    finally:
        app.dependency_overrides.clear()