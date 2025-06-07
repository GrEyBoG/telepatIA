from abc import ABC, abstractmethod
import datetime
import logging
import asyncio
from agents import InputGuardrailTripwireTriggered, TResponseInputItem
# Services
from shared.services import AgentService
# Clients
from shared.clients import OpenAIClient
# Models
from shared.models import AskModel, ResponseBase, HttpStatusCode

class IChatService(ABC):
    @abstractmethod
    async def get_agent_response(self, user_input: str) -> str:
        #---------------------------------------------------------------------------
        # *                           get_agent_response
        # ? Get the response from the agent
        # @param user_input type str  The user input to send to the agent
        # @return type str  The response from the agent
        #---------------------------------------------------------------------------
        pass
    
class ChatService(IChatService):
    def __init__(self, agent: AgentService, logger: logging.Logger, openai_client: OpenAIClient):
        self.logger = logger
        self.agent = agent
        self.openai_client = openai_client
        self.convo_items: list[TResponseInputItem] = []

    async def get_agent_response(self, request: AskModel) -> ResponseBase:
        #---------------------------------------------------------------------------
        # *                           get_agent_response
        # ?  @brief Get the response from the agent
        # @param user_input type str  The user input to send to the agent
        # @return type str  The response from the agent
        #---------------------------------------------------------------------------
        if not self.agent._initialized:
            await self.agent._setup()
        try:
            if request.audio_url:
                content = f'{request.message}\n\n[Audio URL: {request.audio_url}]'
            else:
                content = request.message

            self.convo_items.append({
                "type": "message",
                "content": content,
                "role": "user"
            })

            filtered_input = [
                item for item in self.convo_items if item.get('type') == 'message'
            ]

            trace_description = f'TelepatIA - {datetime.datetime.now().isoformat()}'
            response = await self.openai_client.run_agent(
                self.agent.manager_agent, 
                user_input=filtered_input, 
                trace_description=trace_description, 
            )

            if response.last_agent.name != "Diagnostic Agent":
                self.convo_items.append({
                    "type": "message",
                    "content": response.final_output,
                    "role": "assistant"
                })
            else:
                self.convo_items.clear()  # Se resetea la conversación
                

            return ResponseBase(
                Message="Successfully processed your request.",
                HttpStatusCode=HttpStatusCode.OK.value,
                response=response.final_output
            )

        except Exception as e:
            self.logger.error(f"Error getting agent response: {e}")
            return ResponseBase(
                Message="An error occurred while processing your request.",
                HttpStatusCode=HttpStatusCode.INTERNAL_SERVER_ERROR.value,
                response=str(e)
            )