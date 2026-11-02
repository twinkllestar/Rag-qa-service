# Dependencies:集中管理 "用哪个 retriever / LLM"。
from openai import OpenAI

from app.core.config import settings
from app.services.llm import LLM, AzureOpenAILLM, FakeLLM
from app.services.retrieval import FakeRetriever, Retriever


def get_retriever() -> Retriever:
    return FakeRetriever()


def get_llm() -> LLM:
    if settings.llm_backend == "azure":
        client = OpenAI(
            base_url=settings.azure_openai_endpoint,
            api_key=settings.azure_openai_api_key,
        )
        return AzureOpenAILLM(client, settings.azure_openai_chat_deployment)
    return FakeLLM()