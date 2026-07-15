"""Pydantic schemas for the AI Assistant endpoint.

Schemas
-------
AiQueryRequest  — POST /ai/query request body.
AiQueryResponse — POST /ai/query response body.
"""

from typing import Any

from pydantic import BaseModel, Field


class AiQueryRequest(BaseModel):
    """Natural-language question submitted to the AI assistant.

    The query is processed by the LLM-based intent detector or the
    fallback regex-based keyword parser.
    """

    query: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Natural-language question about seats, employees, or projects.",
        examples=[
            "Where is employee Amit seated?",
            "Show all available seats on Floor 3.",
            "How many seats are occupied for Project Talos?",
        ],
    )


class AiQueryResponse(BaseModel):
    """Response from the AI assistant.

    ``answer`` contains the natural-language reply.
    ``data`` optionally holds structured data that the frontend
    can render (e.g., a list of available seats).
    """

    answer: str = Field(
        ...,
        description="Natural-language response to the user's query.",
    )
    data: dict[str, Any] | None = Field(
        None,
        description="Optional structured data backing the answer.",
    )
