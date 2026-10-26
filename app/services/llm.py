# LLM:根据 question 和检索到的 sources 生成 answer
from typing import Protocol

from app.schemas.ask import Source


class LLM(Protocol):
    def generate(self, question: str, sources: list[Source]) -> str: ...


class FakeLLM:
    # 假的版本:不调用任何模型,只把检索到的内容拼成一个 answer
    def generate(self, question: str, sources: list[Source]) -> str:
        if not sources:
            return "I don't know based on the provided documents."
        return f"Based on {sources[0].doc_id}: {sources[0].text}"