from abc import ABC, abstractmethod
import asyncio
import logging
# Clients
from shared.clients import OpenAIClient
# Models
from shared.models import DiagnosisModel
# Helpers
from shared.helpers import _load_prompt

class IAgentService(ABC):
    @abstractmethod
    async def _setup(self):
        #---------------------------------------------------------------------------
        # *                           _setup
        # ?  @brief Setup the agent service
        # @param name type str  The name of the agent
        # @param name type str  The name of the agent
        # @return type None
        #---------------------------------------------------------------------------
        pass

class AgentService(IAgentService):
    
    def __init__(self, openai_client: OpenAIClient, logger: logging.Logger, tools: list[callable]):
        self.logger = logger
        self.openai_client = openai_client
        self._init_lock = asyncio.Lock()
        self._initialized = False
        self._tools = tools
        
    #---------------------------------------------------------------------------
    #                            Init
    #---------------------------------------------------------------------------
    async def _setup(self):
        #---------------------------------------------------------------------------
        # *                           _setup
        # ?  @brief Setup the agent service
        # @param name type str  The name of the agent
        # @param name type str  The name of the agent
        # @return type None
        #---------------------------------------------------------------------------
        async with self._init_lock:
            if self._initialized:
                return
            
        self.diagnostic_agent = await self.openai_client.create_agent(
            name="Diagnostic Agent",
            handoff_description="This agent receives structured medical data and returns a clear diagnosis, a treatment plan, and specific health recommendations.",
            instructions= await _load_prompt("diagnostic_agent_prompt.txt"),
            output_type=DiagnosisModel,
            
        )
        self.extractor_agent = await self.openai_client.create_agent(
            name="Extractor Agent",
            handoff_description="This agent handles both transcription of audio inputs and extraction of structured medical data (symptoms, patient info, reason for consultation). It actively interacts with the user to fill any missing fields in the medical profile.",
            instructions= await _load_prompt("extractor_agent_prompt.txt"),
            tools=[
                *self._tools['extractor_tools'],
            ],
            handoffs=[
                self.diagnostic_agent,
            ],
        )
        self.manager_agent = await self.openai_client.create_agent(
            name="Manager Agent",
            instructions= await _load_prompt("manager_agent_prompt.txt"),
            handoffs=[
                self.extractor_agent,
            ],
            input_guardrails=[
                *self._tools['guardrail_tools'],
            ],
        )
        self._initialized = True
        
    
