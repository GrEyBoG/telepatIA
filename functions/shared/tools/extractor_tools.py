from agents import RunContextWrapper, function_tool
import logging
from typing import Any, List
# Models
from shared.models import DataModel, PatientInfo
# Clients
from shared.clients import OpenAIClient

def create_extractor_tools(openai_client: OpenAIClient, logger: logging.Logger):
    #---------------------------------------------------------------------------
    # *                           create_extractor_tools
    # ?  @brief Create extractor tools for the agent
    # @param client type OpenAIClient  The OpenAI client instance
    # @param logger type logging.Logger  The logger instance
    # @return type list[callable]  List of extractor tools
    #---------------------------------------------------------------------------
    @function_tool(strict_mode=False)
    async def transcript_audio(wrapper: RunContextWrapper[Any], audio_url: str) -> str:
        """
        Use this tool to transcribe audio input using OpenAI's transcription service.
        The audio file should be accessible via the provided URL.
        """
        #---------------------------------------------------------------------------
        # *                           transcript_audio
        # ?  @brief Transcribe audio input using OpenAI's transcription service
        # @param audio_url type str  The URL of the audio file to transcribe
        # @return type str  The transcribed text
        #---------------------------------------------------------------------------
        logger.info("Transcribing audio input.")
        return await openai_client.transcript_audio(audio_url)
    @function_tool(strict_mode=False)
    async def retrieve_medical_data(wrapper: RunContextWrapper[Any], user_id: str, name: str, age: int, symptoms: List[str], reason_for_consultation: str) -> DataModel:
        """
        Use this tool to extract structured medical data from the provided text.
        The function will create a DataModel instance containing the patient's information,
        symptoms, and reason for consultation.
        """
        #---------------------------------------------------------------------------
        # *                           retrieve_medical_data
        # ?  @brief Retrieve structured medical data for a patient
        # @param user_id type str  The ID of the user
        # @param name type str  The name of the patient
        # @param age type int  The age of the patient
        # @param symptoms type list[str]  The symptoms reported by the patient
        # @param reason_for_consultation type str  The reason for the consultation
        # @return type DataModel  The retrieved medical data
        #---------------------------------------------------------------------------
        logger.info("Retrieving medical data.")
        patient_info = PatientInfo(id=user_id, name=name, age=age)
        return DataModel(
            symptoms=symptoms,
            patient_info=patient_info,
            reason_for_consultation=reason_for_consultation
        )
    
    return [
        transcript_audio,
        retrieve_medical_data
    ]