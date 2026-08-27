from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Pertanyaan natural language dari user.")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Jawaban yang di-generate, digroundkan ke data inventory asli.")
