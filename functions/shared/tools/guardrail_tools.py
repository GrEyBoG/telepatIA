import asyncio
from typing import Any
from agents import function_tool, RunContextWrapper, FunctionTool, Agent, TResponseInputItem, GuardrailFunctionOutput, input_guardrail, trace
import logging
# Models
from shared.models import GuardrailModel
# Clients
from shared.clients import OpenAIClient

def create_guardrail_tools(logger: logging.Logger, guardrail_agent: Agent, openai_client: OpenAIClient) -> list[callable]:
    """
    Create guardrail tools for the application.
    These tools are used to ensure that the application adheres to certain rules and guidelines.
    """
    _cached_agent: Agent | None = None
    _lock = asyncio.Lock()
    
    async def _get_agent() -> Agent:
        nonlocal _cached_agent
        async with _lock:
            if _cached_agent is None:
                if hasattr(guardrail_agent, "__aenter__"):
                    _cached_agent = await guardrail_agent.__aenter__()
                else:
                    _cached_agent = guardrail_agent
            return _cached_agent
    
    @input_guardrail()
    async def scan_input(wrapper: RunContextWrapper[Any], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
        """
        Scan the input for any violations of the guardrails.
        If any violations are found, return a GuardrailFunctionOutput with the violations.
        Otherwise, return a GuardrailFunctionOutput with no violations.
        """
        
        g_agent = await _get_agent()
        detection_result = await openai_client.run_agent(agent=g_agent, user_input=input)
        
        logger.info(f'Guardrail scan result: {detection_result.final_output}')
        
        return GuardrailFunctionOutput(
            tripwire_triggered=detection_result.final_output.block,
            output_info=detection_result.final_output.info
        )
    
    return [scan_input]
        