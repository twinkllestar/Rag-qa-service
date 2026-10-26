# Request / response 的数据格式。FastAPI 用它们做 validation 和生成 /docs
# BaseModel is used for data validation and serialization in FastAPI.
# It allows you to define the structure of your request and response data,
# ensuring that the data adheres to the specified format and constraints. 
# The Field class is used to provide additional metadata and validation rules for individual fields in the model.
from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    # min_length / max_length are basic input validation
    question: str = Field(min_length=1, max_length=1000)


class Source(BaseModel):
    doc_id: str
    text: str
    score: float


class AskResponse(BaseModel):
    answer: str
    sources: list[Source]