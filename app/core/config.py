# 读取配置:从环境变量或 .env 文件加载,避免把配置写死在代码里
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "dev"

    # Azure OpenAI。默认空字符串,这样没有 .env 时 (比如 CI 里跑 test) 也不会 crash
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_chat_deployment: str = "chat"
    azure_openai_embedding_deployment: str = "embedding"

    # Azure AI Search
    azure_search_endpoint: str = ""
    azure_search_api_key: str = ""
    azure_search_index: str = "docs"

    # fake / azure:用哪种实现。test 和 CI 默认用 fake,不花钱
    llm_backend: str = "fake"
    retriever_backend: str = "fake"
        # key / identity:云端用 identity (没有任何 key),本地用 key
    auth_mode: str = "key"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()