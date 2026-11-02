# read settings from .env file. If .env file does not exist, use default values.
# This is useful for CI/CD pipelines where we don't want to commit secrets to the repo.
from pydantic_settings import BaseSettings, SettingsConfigDict

# BaseSettings可不区分大小写 识别任何大小写只需字母一样即可
class Settings(BaseSettings):
    app_env: str = "dev"

    # Azure OpenAI 默认空字符串,这样没有 .env 时 (比如 CI 里跑 test) 也不会 crash
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_chat_deployment: str = "chat"
    azure_openai_embedding_deployment: str = "embedding"

    # fake / azure:用哪种 LLM。test 和 CI 默认用 fake,不花钱
    llm_backend: str = "fake"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()