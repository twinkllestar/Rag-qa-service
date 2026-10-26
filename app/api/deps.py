# Dependencies:集中管理 "用哪个 retriever / LLM"。
# 以后换成 Azure 版本,只需要改这一个文件
from app.services.llm import LLM, FakeLLM
from app.services.retrieval import FakeRetriever, Retriever


def get_retriever() -> Retriever:
    return FakeRetriever()


def get_llm() -> LLM:
    return FakeLLM()