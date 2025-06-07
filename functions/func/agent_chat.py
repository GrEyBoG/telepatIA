# chat_agent.py
from firebase_functions import https_fn, params
from flask import Request
from dotenv import load_dotenv
import os, json, asyncio

# Init
from shared.firebase_init import firebase_app
from shared.helpers import setup_logging, MethodInterceptor, _load_prompt
from shared.models import AskModel, ResponseBase, GuardrailModel
from shared.clients import OpenAIClient
from shared.services import AgentService, ChatService
from shared.tools import create_extractor_tools, create_guardrail_tools

#---------------------------
#     SetUp
#---------------------------
load_dotenv()
logger = setup_logging()
openai_api_key = os.getenv("OPENAI_API_KEY") or params.config().openai.api_key
openai_model = os.getenv("OPENAI_MODEL") or params.config().openai.model
openai_client = OpenAIClient(api_key=openai_api_key, model=openai_model, logger=logger)

#---------------------------
#     Guardrail Agent
#---------------------------
async def create_guardrail_agent():
    return await openai_client.create_agent(
        name="Content Guardrail Agent",
        handoff_description="Moderates all content to prevent harmful requests.",
        instructions=await _load_prompt("guardrail_agent_prompt.txt"),
        output_type=GuardrailModel,
    )
guardrail_agent = asyncio.run(create_guardrail_agent())

#---------------------------
#     Tools
#---------------------------
extractor_tools = create_extractor_tools(openai_client=openai_client, logger=logger)
guardrail_tools = create_guardrail_tools(openai_client=openai_client, logger=logger, guardrail_agent=guardrail_agent)
tools = {
    "extractor_tools": extractor_tools,
    "guardrail_tools": guardrail_tools
}

#---------------------------
#     Services
#---------------------------
agent_service = AgentService(openai_client=openai_client, logger=logger, tools=tools)
chat_service = ChatService(agent=agent_service, logger=logger, openai_client=openai_client)

#---------------------------
#     Cloud Function
#---------------------------
@https_fn.on_request()
def chat_agent(req: https_fn.Request) -> https_fn.Response:
    try:
        
        body = req.get_json()
        ask_model = AskModel(**body)

        if not ask_model.message and not ask_model.audio_url:
            return https_fn.Response(json.dumps({"detail": "message or audio_url is required"}), status=422, mimetype="application/json")

        async def method():
            return await chat_service.get_agent_response(request=ask_model)

        result = asyncio.run(MethodInterceptor.execute(request=req, custom_method=method))
        return https_fn.Response(result.json(), mimetype="application/json")

    except Exception as e:
        return https_fn.Response(json.dumps({"error": str(e)}), status=500, mimetype="application/json")
