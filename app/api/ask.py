# POST /ask:接收question, 返回 answer 和 sources
from fastapi import APIRouter, Depends

from app.api.deps import get_llm, get_retriever
from app.schemas.ask import AskRequest, AskResponse
from app.services.llm import LLM
from app.services.retrieval import Retriever

router = APIRouter()

# /ask is the interface path 

@router.post("/ask", response_model=AskResponse)
def ask(
    req: AskRequest,
    retriever: Retriever = Depends(get_retriever),
    llm: LLM = Depends(get_llm),
) -> AskResponse:
    sources = retriever.search(req.question)
    answer = llm.generate(req.question, sources)
    return AskResponse(answer=answer, sources=sources)