"""AI Assistant API route (Placeholder for Phase 14)."""

from fastapi import APIRouter

from app.schemas.ai import AiQueryRequest, AiQueryResponse

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


@router.post(
    "/query",
    response_model=AiQueryResponse,
    summary="Query the AI assistant",
)
def query_ai_assistant(data: AiQueryRequest) -> AiQueryResponse:
    """Natural language interface for querying the seat allocation system.

    Note: The actual LLM integration logic belongs in Phase 14.
    This endpoint currently serves as a schema-compliant placeholder.
    """
    return AiQueryResponse(
        answer="The AI assistant logic will be implemented in Phase 14. "
        "Your query was received successfully.",
        data={"query": data.query},
    )
