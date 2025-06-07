from pydantic import BaseModel, Field
from typing import Optional

class AskModel(BaseModel):
    message: Optional[str] = Field(
        None,
        description="The message or question to be sent to the agent."
    )
    audio_url: Optional[str] = Field(
        None,
        description="Optional URL of an audio file to be sent to the agent."
    )