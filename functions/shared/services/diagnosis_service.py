from abc import ABC, abstractmethod
import logging
# Clients
from shared.clients import OpenAIClient
# Models
from shared.models import ResponseBase, HttpStatusCode, DataModel, DiagnosisModel
# Helpers
from shared.helpers import _load_prompt

class IDiagnosisService(ABC):
    @abstractmethod
    async def diagnose(self, patient_info: dict) -> ResponseBase:
        #---------------------------------------------------------------------------
        # *                           diagnose
        # ?  Generate a diagnosis based on patient information
        # @param patient_info type dict  The patient information to use for diagnosis
        # @return type ResponseBase  The response containing the diagnosis
        #---------------------------------------------------------------------------
        pass
    
class DiagnosisService(IDiagnosisService):
    def __init__(self, openai_client: OpenAIClient, logger: logging.Logger):
        self.openai_client = openai_client
        self.logger = logger

    async def diagnose(self, patient_info: DataModel) -> ResponseBase:
        self.logger.info(f"Generating diagnosis for patient info: {patient_info}")
        try:
            prompt = await _load_prompt("diagnosis_prompt.txt")
            response = await self.openai_client.get_generic_model_response(
                text_format=DiagnosisModel,
                instructions=prompt,
                input=patient_info
            )
            return ResponseBase(
                Message="Diagnosis generated successfully",
                HttpStatusCode=HttpStatusCode.OK.value,
                response=response
            )
        except Exception as e:
            self.logger.error(f"Error generating diagnosis: {e}")
            return ResponseBase(
                Message="Error generating diagnosis",
                HttpStatusCode=HttpStatusCode.INTERNAL_SERVER_ERROR.value,
                response=str(e)
            )