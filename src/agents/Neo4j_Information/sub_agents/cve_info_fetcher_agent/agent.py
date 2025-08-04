import webbrowser
from google.adk.agents import Agent, LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.genai.client import Client
from google.adk.agents import SequentialAgent

# CVE Information Fetcher Agent
# Takes the initial specification (from user query) and fetches CVE information.
cve_info_fetcher_agent = LlmAgent(
    name="cve_info_fetcher_agent",
    model='gemini-2.0-flash',
    instruction="""You are a CVE information provider. Given a CVE, you should:
1. Search for relevant information about the CVE.
2. Provide a brief description of the CVE.
3. Provide the severity and affected products of the CVE.
4. Provide any relevant links or references for the CVE.
""", 
    description="Fetches information about a CVE.",
    output_key="cve_info"
)

