from firebase_functions import params
from firebase_functions import https_fn
from flask import Request
import json
import asyncio
from shared.firebase_init import firebase_app
import os
from dotenv import load_dotenv
# Models
from shared.models import RequestModel, ResponseBase
# Clients
from shared.clients import OpenAIClient
# Services
from shared.services import AudioTranscriptService
# Helpers
from shared.helpers import MethodInterceptor, setup_logging

#---------------------------
#     SetUp
#---------------------------
load_dotenv()
logger = setup_logging()
openai_api_key = os.getenv("OPENAI_API_KEY") or params.config().openai.api_key
openai_model = os.getenv("OPENAI_MODEL") or params.config().openai.model
# Clients
openai_client = OpenAIClient(api_key=openai_api_key, model=openai_model, logger=logger)
# Services
AudioTranscriptService = AudioTranscriptService(openai_client=openai_client, logger=logger)

@https_fn.on_request()
def transcribe_audio(req: https_fn.Request) -> https_fn.Response:
    try:
        body = req.get_json()
        request_model = RequestModel(**body)

        if not request_model.audio_url:
            return https_fn.Response(json.dumps({"detail": "audio_url is required"}), status=422, mimetype="application/json")

        async def method():
            return await AudioTranscriptService.transcribe_audio(
                audio_url=request_model.audio_url
            )

        result = asyncio.run(MethodInterceptor.execute(request=req, custom_method=method))

        return https_fn.Response(result.json(), mimetype="application/json")

    except Exception as e:
        return https_fn.Response(json.dumps({"error": str(e)}), status=500, mimetype="application/json")
