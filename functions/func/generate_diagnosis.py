from dotenv import load_dotenv
from firebase_functions import https_fn
from firebase_functions import params
from firebase_admin import initialize_app
from flask import Request
import asyncio
import json, os
from shared.firebase_init import firebase_app
# Models
from shared.models import RequestModel
# Clients
from shared.clients import OpenAIClient
# Services
from shared.services import DiagnosisService
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
DiagnosisService = DiagnosisService(openai_client=openai_client, logger=logger)

@https_fn.on_request()
def generate_diagnosis(req: https_fn.Request) -> https_fn.Response:
    try:
        body = req.get_json()
        request_model = RequestModel(**body)

        if not request_model.data:
            return https_fn.Response(json.dumps({"detail": "patient_info is required"}), status=422, mimetype='application/json')

        async def method():
            return await DiagnosisService.diagnose(
                patient_info=request_model.data
            )

        result = asyncio.run(MethodInterceptor.execute(request=req, custom_method=method))
        return https_fn.Response(result.json(), mimetype='application/json')

    except Exception as e:
        return https_fn.Response(json.dumps({"error": str(e)}), status=500, mimetype='application/json')