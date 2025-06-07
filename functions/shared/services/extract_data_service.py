from abc import ABC, abstractmethod
import logging
# Clients
from shared.clients import OpenAIClient
# Models
from shared.models import ResponseBase, HttpStatusCode, DataModel, PatientInfo
# Helpers
from shared.helpers import _load_prompt

class IExtractDataService(ABC):
    @abstractmethod
    async def extract_data(self, input_text: str) -> ResponseBase:
        #---------------------------------------------------------------------------
        # *                           extract_data
        # ?  Extract data from the given input text
        # @param input_text type str  The input text to extract data from
        # @return type ResponseBase  The response containing the extracted data
        #---------------------------------------------------------------------------
        pass
    
class ExtractDataService(IExtractDataService):
    def __init__(self, openai_client: OpenAIClient, logger: logging.Logger):
        self.openai_client = openai_client
        self.logger = logger

    async def extract_data(self, input: str) -> ResponseBase:
        self.logger.info("Extracting data from input")
        try:
            prompt = await _load_prompt("data_extractor_prompt.txt")
            response = await self.openai_client.get_generic_model_response(text_format=DataModel, instructions=prompt, input=input)
            return ResponseBase(
                Message="Data extracted successfully",
                HttpStatusCode=HttpStatusCode.OK.value,
                response=response
            )
        except Exception as e:
            self.logger.error(f"Error extracting data: {e}")
            return ResponseBase(
                Message="Error extracting data",
                HttpStatusCode=HttpStatusCode.INTERNAL_SERVER_ERROR.value,
                response=str(e)
            )