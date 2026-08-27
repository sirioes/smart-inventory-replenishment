from fastapi import APIRouter, Depends

from api.dependencies import get_answer_inventory_query_use_case
from api.schemas.chat_schema import ChatRequest, ChatResponse
from application.use_cases.answer_inventory_query import AnswerInventoryQueryUseCase

router = APIRouter(tags=["chat"])

@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Ask a natural language question about current inventory",
)
def chat(
    request: ChatRequest,
    use_case: AnswerInventoryQueryUseCase = Depends(get_answer_inventory_query_use_case),
) -> ChatResponse:
    answer = use_case.execute(question=request.question)
    return ChatResponse(answer=answer)
