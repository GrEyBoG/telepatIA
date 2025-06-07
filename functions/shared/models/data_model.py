from pydantic import BaseModel, Field
from typing import List

class PatientInfo(BaseModel):
    id: str = Field(
        ...,
        description="Unique identifier for the patient."
        )
    name: str = Field(
        ...,
        description="Name of the patient."
    )
    age: int = Field(
        ...,
        description="Age of the patient."
    )

class DataModel(BaseModel):
    symptoms: List[str] = Field(
        default_factory=list,
        description="List of symptoms associated with the data model."
    )
    patient_info: PatientInfo = Field(
        ...,
        description="Information about the patient."
    )
    reason_for_consultation: str = Field(
        ...,
        description="Reason for the patient's consultation."
    )