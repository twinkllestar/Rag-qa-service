# Dependencies:集中管理 "用哪个 retriever / LLM"。
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from openai import OpenAI

from app.core.config import settings
from app.services.llm import LLM, AzureOpenAILLM, FakeLLM
from app.services.retrieval import AzureSearchRetriever, FakeRetriever, Retriever


def _openai_client() -> OpenAI:
    return OpenAI(
        base_url=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
    )


def get_retriever() -> Retriever:
    if settings.retriever_backend == "azure":
        search_client = SearchClient(
            endpoint=settings.azure_search_endpoint,
            index_name=settings.azure_search_index,
            credential=AzureKeyCredential(settings.azure_search_api_key),
        )
        return AzureSearchRetriever(
            search_client,
            _openai_client(),
            settings.azure_openai_embedding_deployment,
        )
    return FakeRetriever()


def get_llm() -> LLM:
    if settings.llm_backend == "azure":
        return AzureOpenAILLM(_openai_client(), settings.azure_openai_chat_deployment)
    return FakeLLM()