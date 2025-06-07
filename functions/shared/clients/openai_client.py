from abc import ABC, abstractmethod
from typing import Any, Sequence
from openai import AsyncOpenAI, BaseModel
from agents import Agent, Runner, TResponseInputItem, get_current_trace, set_default_openai_client, InputGuardrail, trace
from shared.models import ResponseBase
import logging
# Helpers
from shared.helpers import download_audio, delete_audio_file

class IOpenAIClient(ABC):
    @abstractmethod
    async def create_agent(self, name: str, handoff_description: str, instructions: str, output_type: None, handoffs: None, input_guardrails: None) -> Agent:
        #---------------------------------------------------------------------------
        # *                           create_agent
        # ?  @brief Create a new agent
        # @param name type str  The name of the agent
        # @param name type str  The name of the agent
        # @param handoff_description type str  The handoff description of the agent
        # @param instructions type str  The instructions for the agent
        # @param output_type type None
        # @return type Agent  The created agent
        #---------------------------------------------------------------------------
        pass
    
    @abstractmethod
    async def run_agent(self, agent: Agent, user_input: str) -> ResponseBase:
        #---------------------------------------------------------------------------
        # *                           run_agent
        # ?  @brief Run an agent with the given input
        # @param agent type Agent  The agent to run
        # @param input type str  The input to the agent
        # @return type ResponseBase  The response from the agent
        #---------------------------------------------------------------------------
        pass
    
    @abstractmethod
    async def transcript_audio(self, audio_file: str) -> str:
        #---------------------------------------------------------------------------
        # *                           transcript_audio
        # ?  @brief Transcribe audio to text using OpenAI's Whisper model
        # @param audio_file type str  The path to the audio file
        # @return type str  The transcribed text
        #---------------------------------------------------------------------------
        pass
    
    @abstractmethod
    async def get_generic_model_response(self, model: str | None = None, text_format: BaseModel | None = None, instructions: str | None = None, input: str | BaseModel | None = None) -> ResponseBase:
        #---------------------------------------------------------------------------
        # *                           create_generic_model
        # ?  @brief Create a generic model for the agent
        # @param model type str  The model to use for the agent
        # @param text_format type Any  The text format for the model
        # @param input type Any  The input for the model
        # @return type ResponseBase  The created response base
        #---------------------------------------------------------------------------
        pass


class OpenAIClient(IOpenAIClient):
    def __init__(self, api_key: str, logger: logging.Logger, model):
        #---------------------------------------------------------------------------
        # *                           __init__
        # ?  @brief Initialize the OpenAI API client
        # @param api_key type str  OpenAI API Key
        # @param logger type Logger  Logging instance
        #---------------------------------------------------------------------------
        self.logger = logger
        self.client = AsyncOpenAI(api_key=api_key)
        set_default_openai_client(self.client)
        self.model = model

    async def create_agent(self, name: str, handoff_description: str | None = None, instructions: str | None = None, output_type: Any | None = None, handoffs: Sequence[Agent] | None = None, input_guardrails: Sequence[InputGuardrail] | None = None, tools: list[Any] | None = None, model: str | None = None) -> Agent:
        #---------------------------------------------------------------------------
        # *                           create_agent
        # ?  @brief Create a new agent
        # @param name type str  The name of the agent
        # @param handoff_description type str  The handoff description of the agent
        # @param instructions type str  The instructions for the agent
        # @param output_type type None
        # @param handoffs type None
        # @param input_guardrails type None
        # @param tools type list[Any]  List of tools for the agent
        # @param model type str  The model to use for the agent, defaults to the client's model
        # @return type Agent  The created agent
        #---------------------------------------------------------------------------
        self.logger.info(f"Creating agent: {name}")
        try:
            agent = Agent(name=name, 
                            handoff_description=handoff_description,   
                            instructions=instructions, 
                            output_type=output_type, 
                            handoffs=handoffs or [], 
                            input_guardrails=input_guardrails or [],
                            model=model or self.model,
                            tools=tools or [],
                          )
            return agent
        except Exception as e:
            self.logger.error(f"Error creating agent: {e}")
            raise e
        
    async def run_agent(self, agent: Agent, user_input: str | list[TResponseInputItem] = [], trace_description: str | None = None, context: Any | None = None) -> ResponseBase:
        #---------------------------------------------------------------------------
        # *                           run_agent
        # ?  @brief Run an agent with the given input
        # @param agent type Agent  The agent to run
        # @param trace_description type str  Description for tracing the agent run
        # @param context type Any  Additional context for the agent run
        # @param user_input type list[TResponseInputItem]  The input to the agent, can be a list of response items
        # @param user_input type str  The input to the agent, can be a single string or a list of response items
        # @return type ResponseBase  The response from the agent
        #---------------------------------------------------------------------------
        self.logger.info(f"Running agent: {agent.name}")
        try:
            if isinstance(user_input, list):
                # Filtrar las respuestas anteriores para enviar solo mensajes relevantes
                filtered_input = [
                    item for item in user_input if item['type'] in ['message'] or 
                    (item['type'] == 'tool_call_item' and 'call_id' not in item.get('status', {}))
                ]
            else:
                filtered_input = user_input

            if trace_description and get_current_trace() is None:
                with trace(trace_description):
                    response = await Runner.run(
                        starting_agent=agent, 
                        input=filtered_input, 
                        context=context
                    )
                    self.logger.info(f"Agent Handoff: {response.last_agent.name}")
                    return response
            else:
                response = await Runner.run(
                    starting_agent=agent, 
                    input=filtered_input, 
                    context=context
                )
                self.logger.info(f"Agent Handoff: {response.last_agent.name}")
                return response
        except Exception as e:
            self.logger.error(f"Error running agent: {e}")
            raise e
        
    async def transcript_audio(self, audio_url: str) -> str:
        #---------------------------------------------------------------------------
        # *                           transcript_audio
        # ?  @brief Transcribe audio to text using OpenAI's Whisper model
        # @param audio_file type str  The path to the audio file
        # @return type str  The transcribed text
        #---------------------------------------------------------------------------
        self.logger.info(f"Transcribing audio file: {audio_url}")
        try:
            local_path: Path = await download_audio(audio_url)
            transcription = await self.client.audio.transcriptions.create(
                file=local_path,
                model="gpt-4o-transcribe",
            ) 
            delete_audio_file(local_path)
            self.logger.info("Audio transcription completed successfully")
            return transcription.text
        except Exception as e:
            self.logger.error(f"Error transcribing audio: {e}")
            raise e
        
        
    async def get_generic_model_response(self, model: str | None = None, text_format: BaseModel | None = None, instructions: str | None = None, input: str | BaseModel | None = None) -> ResponseBase:
        #---------------------------------------------------------------------------
        # *                           get_generic_model_response
        # ?  @brief Get a generic model response from OpenAI
        # @param model type str  The model to use for the response
        # @param text_format type BaseModel  The text format for the response
        # @param instructions type str  The system instructions for the model
        # @param input type str | BaseModel  The input for the model
        # @return type ResponseBase  The parsed response from the model
        #---------------------------------------------------------------------------
        self.logger.info("Getting generic model response")
        if isinstance(input, BaseModel):
            user_content = input.model_dump_json()
        else:
            user_content = str(input)
        response = await self.client.responses.parse(
            model=model or self.model,
            input=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": user_content}
            ],
            text_format=text_format
        )
        return response.output_parsed
    
    
