from abc import ABC, abstractmethod
import logging
# Clients
from shared.clients import OpenAIClient
# Models
from shared.models import ResponseBase, HttpStatusCode

class IAudioTranscriptService(ABC):
    @abstractmethod
    async def transcribe_audio(self, audio_url: str) -> ResponseBase:
        #---------------------------------------------------------------------------
        # *                           transcribe_audio
        # ?  Transcribe an audio file from a given URL
        # @param audio_url type str  The URL of the audio file to transcribe
        # @return type ResponseBase  The response containing the transcription
        #---------------------------------------------------------------------------
        pass

class AudioTranscriptService(IAudioTranscriptService):
    def __init__(self, openai_client: OpenAIClient, logger: logging.Logger):
        self.openai_client = openai_client
        self.logger = logger

    async def transcribe_audio(self, audio_url: str) -> ResponseBase:
        try:
            transcription = await self.openai_client.transcript_audio(audio_url)
            return ResponseBase(
                Message="Audio transcription successful",
                HttpStatusCode=HttpStatusCode.OK.value,
                response=transcription
            )
        except Exception as e:
            self.logger.error(f"Error transcribing audio: {e}")
            return ResponseBase(
                Message="Error transcribing audio",
                HttpStatusCode=HttpStatusCode.INTERNAL_SERVER_ERROR.value,
                response=str(e)
            )