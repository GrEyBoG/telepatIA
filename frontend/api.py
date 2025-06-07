#---------------------------
#     API WRAPPERS
#---------------------------
import requests
from models import ResponseBase, AskModel, RequestModel

API_BASE = "http://127.0.0.1:5001/telepatia-backend/us-central1"

#---------------------------------------------------------------------------
# *                POST REQUEST WITH VALIDATION
# ?  Sends validated input and parses output using ResponseBase
# @param endpoint str  
# @param data dict  
# @return dict
#---------------------------------------------------------------------------
def post_request(endpoint: str, data: dict) -> ResponseBase:
    url = f"{API_BASE}/{endpoint}"
    res = requests.post(url, json=data)
    parsed = ResponseBase(**res.json())
    return parsed

def call_agent_model(message: str, audio_url: str):
    model = AskModel(message=message, audio_url=audio_url)
    return post_request("chat_agent", model.model_dump())

def transcribe_audio_url(audio_url: str):
    req = RequestModel(audio_url=audio_url)
    return post_request("transcribe_audio", req.model_dump())

def extract_from_input(input_text: str):
    req = RequestModel(input_text=input_text)
    return post_request("extract_info", req.model_dump())

def diagnose_from_data(data_model):
    req = RequestModel(data=data_model)
    return post_request("generate_diagnosis", req.model_dump())
