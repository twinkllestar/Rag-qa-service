# 测试 prompt 构造和 AzureOpenAILLM:用 fake client,不碰真实 Azure
from types import SimpleNamespace

from app.schemas.ask import Source
from app.services.llm import AzureOpenAILLM, build_prompt


class FakeOpenAIClient:
    # 模拟 OpenAI client,记录收到的参数,方便 assert
    def __init__(self) -> None:
        self.calls: list[dict] = []
        self.responses = SimpleNamespace(create=self._create)

    def _create(self, **kwargs) -> SimpleNamespace:
        self.calls.append(kwargs)
        return SimpleNamespace(output_text="fake answer [doc-1]")


def make_source() -> Source:
    return Source(doc_id="doc-1", text="Paris is the capital of France.", score=0.9)


def test_build_prompt_wraps_sources_in_document_tags() -> None:
    prompt = build_prompt("What is the capital?", [make_source()])
    assert '<document id="doc-1">' in prompt
    assert "Paris is the capital of France." in prompt
    assert prompt.endswith("Question: What is the capital?")


def test_llm_calls_client_with_system_prompt_and_deployment() -> None:
    client = FakeOpenAIClient()
    llm = AzureOpenAILLM(client, "chat")  # type: ignore[arg-type]
    answer = llm.generate("What is the capital?", [make_source()])
    assert answer == "fake answer [doc-1]"
    assert client.calls[0]["model"] == "chat"
    assert "untrusted DATA" in client.calls[0]["instructions"]


def test_llm_skips_api_call_when_no_sources() -> None:
    client = FakeOpenAIClient()
    llm = AzureOpenAILLM(client, "chat")  # type: ignore[arg-type]
    answer = llm.generate("anything", [])
    assert "don't know" in answer
    assert client.calls == []


# helper for  fake client to return diff anwser
def test_llm_normalizes_refusal_with_extra_citation() -> None:
    client = FakeOpenAIClient()
    client.responses = SimpleNamespace(
        create=lambda **kwargs: SimpleNamespace(
            output_text="I don't know based on the provided documents. [doc-1]"
        )
    )
    llm = AzureOpenAILLM(client, "chat")  # type: ignore[arg-type]
    answer = llm.generate("What is the capital of France?", [make_source()])
    assert answer == "I don't know based on the provided documents."