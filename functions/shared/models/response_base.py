from enum import Enum
from typing import Any
from pydantic import BaseModel

class HttpStatusCode(Enum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500
    
class ResponseBase(BaseModel):
    Message: str
    HttpStatusCode: int
    response: Any = None