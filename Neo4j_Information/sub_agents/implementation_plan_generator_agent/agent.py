import webbrowser
from google.adk.agents import Agent, LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.genai.client import Client
from google.adk.agents import SequentialAgent


# Implementation Plan Generator Agent
# Takes the mitigation plan and generates an implementation plan.
implementation_plan_generator_agent = LlmAgent(
    name="implementation_plan_generator_agent",
    model='gemini-2.0-flash',
    instruction="""You are an implementation plan generator. Given the mitigation plan, you should:
1. Generate a detailed implementation plan.
2. Provide step-by-step instructions for implementing the implementation plan.
3. Provide any relevant links or references for the implementation plan.
4. Don't provide any timeline, but just give a plan or steps.
""", 
    description="Generates an implementation plan.",
    output_key="implementation_plan"
)

