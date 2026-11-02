# Ingestion:读 data/docs 里的文件 → chunking → embedding → 上传到 Azure AI Search
# 运行方式 (在项目根目录): python -m scripts.ingest
import re
import time
from pathlib import Path

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    HnswAlgorithmConfiguration,
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SearchIndex,
    SimpleField,
    VectorSearch,
    VectorSearchProfile,
)
from openai import OpenAI

from app.core.config import settings
from app.services.chunking import chunk_text

EMBEDDING_DIMENSIONS = 1536  # text-embedding-3-small 的 vector 长度
DOCS_DIR = Path("data/docs")
BATCH_SIZE = 10  # 每次 request 只发 10 个 chunks,避免超过 TPM 限额


def build_index() -> SearchIndex:
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True),
        SearchableField(name="content", type=SearchFieldDataType.String),
        SearchField(
            name="embedding",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=EMBEDDING_DIMENSIONS,
            vector_search_profile_name="vec-profile",
        ),
    ]
    vector_search = VectorSearch(
        algorithms=[HnswAlgorithmConfiguration(name="hnsw")],
        profiles=[
            VectorSearchProfile(
                name="vec-profile", algorithm_configuration_name="hnsw"
            )
        ],
    )
    return SearchIndex(
        name=settings.azure_search_index, fields=fields, vector_search=vector_search
    )


def safe_id(name: str) -> str:
    # Azure Search 的 key 只允许字母、数字、_ - =
    return re.sub(r"[^A-Za-z0-9_-]", "-", name)


def embed_all(client: OpenAI, texts: list[str]) -> list[list[float]]:
    # 分批调用 embedding API。client 已设置 max_retries,遇到 429 会自动等待重试
    vectors: list[list[float]] = []
    for start in range(0, len(texts), BATCH_SIZE):
        batch = texts[start : start + BATCH_SIZE]
        response = client.embeddings.create(
            model=settings.azure_openai_embedding_deployment, input=batch
        )
        vectors.extend(item.embedding for item in response.data)
        print(f"Embedded {len(vectors)} / {len(texts)}")
        time.sleep(1)  # 稍微放慢,避免连续触发 rate limit
    return vectors


def main() -> None:
    credential = AzureKeyCredential(settings.azure_search_api_key)
    index_client = SearchIndexClient(settings.azure_search_endpoint, credential)
    index_client.create_or_update_index(build_index())
    print(f"Index '{settings.azure_search_index}' ready")

    chunks: list[tuple[str, str]] = []  # (id, text)
    for path in sorted(DOCS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        for i, chunk in enumerate(chunk_text(text)):
            chunks.append((f"{safe_id(path.stem)}-{i}", chunk))
    print(f"Prepared {len(chunks)} chunks")

    openai_client = OpenAI(
        base_url=settings.azure_openai_endpoint,
        api_key=settings.azure_openai_api_key,
        max_retries=6,
    )
    vectors = embed_all(openai_client, [text for _, text in chunks])

    documents = [
        {"id": chunk_id, "content": text, "embedding": vector}
        for (chunk_id, text), vector in zip(chunks, vectors)
    ]
    search_client = SearchClient(
        settings.azure_search_endpoint, settings.azure_search_index, credential
    )
    result = search_client.upload_documents(documents)
    print(f"Uploaded {sum(1 for r in result if r.succeeded)} / {len(documents)}")


if __name__ == "__main__":
    main()