import webbrowser
from google.adk.agents import Agent, LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.genai.client import Client
from google.adk.agents import SequentialAgent


# TTP Information Fetcher Agent
# Takes the initial specification (from user query) and fetches TTP information.
ttp_info_fetcher_agent = LlmAgent(
    name="ttp_info_fetcher_agent",
    model='gemini-2.0-flash',
    instruction="""You are a TTP information fetcher. Given a TTP, you should:
1. Search for relevant information about the TTP.
2. Provide a brief description of the TTP.
3. Provide the severity and affected products of the TTP.
4. Provide any relevant links or references for the TTP.
""", 
    description="Fetches information about a TTP.",
    output_key="ttp_info"
)
