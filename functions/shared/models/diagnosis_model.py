from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class DiagnosisModel(BaseModel):
    diagnosis: str = Field(
        ...,
        description="The diagnosis made by the healthcare provider."
    )
    treatment: str = Field(
        ...,
        description="The treatment plan recommended for the patient."
    )
    recomendations: str = Field(
        ...,
        description="Additional recommendations for the patient's care."
    )