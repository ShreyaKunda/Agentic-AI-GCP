import webbrowser
from google.adk.agents import Agent, LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.genai.client import Client
from google.adk.agents import SequentialAgent



# CWE Information Fetcher Agent
# Takes the initial specification (from user query) and fetches CWE information.
cwe_info_fetcher_agent = LlmAgent(
    name="cwe_info_fetcher_agent",
    model='gemini-2.0-flash',
    instruction="""You are a CWE information fetcher. Given a CWE, you should:
1. Search for relevant information about the CWE.
2. Provide a brief description of the CWE.
3. Provide the severity and affected products of the CWE.
4. Provide any relevant links or references for the CWE.
""", 
    description="Fetches information about a CWE.",
    output_key="cwe_info"
)
