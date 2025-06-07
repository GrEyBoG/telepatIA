from pydantic import BaseModel, Field
from typing import Optional
from .data_model import DataModel

class RequestModel(BaseModel):
    audio_url: Optional[str] = Field(
        None,
        description="The URL of the audio file to be processed."
    )
    data: Optional[DataModel] = Field(
        None,
        description="The data to be processed."
    )
    input_text: Optional[str] = Field(
        None,
        description="The input text to be processed."
    )