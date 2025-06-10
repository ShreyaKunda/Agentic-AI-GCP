import webbrowser
from google.adk.agents import Agent, LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.genai.client import Client
from google.adk.agents import SequentialAgent


# CAPEC Information Fetcher Agent
# Takes the initial specification (from user query) and fetches CAPEC information.
capec_info_fetcher_agent = LlmAgent(
    name="capec_info_fetcher_agent",
    model='gemini-2.0-flash',
    instruction="""You are a CAPEC information fetcher. Given a CAPEC, you should:
1. Search for relevant information about the CAPEC.
2. Provide a brief description of the CAPEC.
3. Provide the severity and affected products of the CAPEC.
4. Provide any relevant links or references for the CAPEC.
""", 
    description="Fetches information about a CAPEC.",
    output_key="capec_info"
)
