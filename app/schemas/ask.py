# Request / Response schemas for FastAPI endpoints
# FastAPI use them for validation and produce /docs
from pydantic import BaseModel, ConfigDict, Field


class AskRequest(BaseModel):
    # str_strip_whitespace: ruduce whitespaces, then check length
    #  "   " --> "" 
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(min_length=1, max_length=1000)


class Source(BaseModel):
    doc_id: str
    text: str
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]