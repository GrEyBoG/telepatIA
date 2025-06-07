from http.client import HTTPException
import inspect
import logging
from urllib.request import Request
from flask import jsonify, Response
# Helpers
from shared.helpers import setup_logging
# Models
from shared.models import HttpStatusCode

logger = setup_logging()


class MethodInterceptor:
    @staticmethod
    async def execute(request: Request, custom_method):
        try:
            if inspect.iscoroutinefunction(custom_method):
                result = await custom_method()
            else:
                result = custom_method()
            logger.info(f"Method {request.path} executed successfully.")
            return result
        except HTTPException as http_exc:
            logger.error(f"HTTP error in {request.path}: {http_exc.detail}")
            return Response(
                response=jsonify(http_exc.detail),
                status=http_exc.status_code,
            )
        except Exception as e:
            logger.error(f"Error in {request.path}: {e}")
            return Response(
                response=jsonify(f"Error in {request.path}: {e}"),
                status=HttpStatusCode.INTERNAL_SERVER_ERROR.value,
            )
