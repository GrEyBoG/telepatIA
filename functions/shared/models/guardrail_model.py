from pydantic import BaseModel, Field
from typing import Optional

class GuardrailModel(BaseModel):
    block: bool = Field(
        description="Whether to block the response if it violates the guardrail.",
    )
    info: Optional[str] = Field(
        default=None,
        description="Information about the guardrail violation.",
    )