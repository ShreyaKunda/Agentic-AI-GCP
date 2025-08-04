import webbrowser
from google.adk.agents import Agent, LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.genai.client import Client
from google.adk.agents import SequentialAgent



# Mitigation Plan Generator Agent
# Takes the CVE, CWE, CAPEC, and TTP information and generates a mitigation plan.
mitigation_plan_generator_agent = LlmAgent(
    name="mitigation_plan_generator_agent",
    model='gemini-2.0-flash',
    instruction="""You are a mitigation plan generator. Given the CVE, CWE, CAPEC, and TTP information, you should:
1. Generate a detailed mitigation plan.
2. Provide step-by-step instructions for implementing the mitigation plan.
3. Provide any relevant links or references for the mitigation plan.
4. Don't provide any timeline, but just give a plan or steps.
""", 
    description="Generates a mitigation plan.",
    output_key="mitigation_plan"
)
