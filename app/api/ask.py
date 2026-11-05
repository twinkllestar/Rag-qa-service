# POST /ask:recive question, safety check, then retun answer 和 sources
import logging

from fastapi import APIRouter, Depends, HTTPException, Request

from app.api.deps import get_llm, get_retriever
from app.schemas.ask import AskRequest, AskResponse
from app.services.guard import looks_like_injection, redact_pii
from app.services.llm import LLM
from app.services.retrieval import Retriever

router = APIRouter()
logger = logging.getLogger("app.ask")


@router.post("/ask", response_model=AskResponse)
def ask(
    req: AskRequest,
    request: Request,
    retriever: Retriever = Depends(get_retriever),
    llm: LLM = Depends(get_llm),
) -> AskResponse:
    request_id = request.state.request_id  # 由 middleware 设置

    # 1. Injection filter: log 里只记 request_id,不记 question 原文
    if looks_like_injection(req.question):
        logger.warning("request_id=%s blocked=injection", request_id)
        raise HTTPException(
            status_code=400,
            detail="Your question was blocked by the input safety filter.",
        )

    # 2. PII redaction:后面的 retriever 和 LLM 只会看到脱敏后的 question
    question, pii_count = redact_pii(req.question)
    if pii_count:
        logger.info("request_id=%s pii_redacted=%d", request_id, pii_count)

    # 3. 正常的 RAG 流程
    sources = retriever.search(question)
    answer = llm.generate(question, sources)
    return AskResponse(answer=answer, sources=sources)