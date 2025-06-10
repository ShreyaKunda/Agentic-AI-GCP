import webbrowser
from google.adk.agents import Agent, LlmAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.genai.client import Client
from google.adk.agents import SequentialAgent
from Neo4j_Information.sub_agents.cve_info_fetcher_agent.agent import cve_info_fetcher_agent
from Neo4j_Information.sub_agents.cwe_info_fetcher_agent.agent import cwe_info_fetcher_agent
from Neo4j_Information.sub_agents.capec_info_fetcher_agent.agent import capec_info_fetcher_agent
from Neo4j_Information.sub_agents.ttp_info_fetcher_agent.agent import ttp_info_fetcher_agent
from Neo4j_Information.sub_agents.mitigation_plan_generator_agent.agent import mitigation_plan_generator_agent
from Neo4j_Information.sub_agents.implementation_plan_generator_agent.agent import implementation_plan_generator_agent

# --- 2. Create the SequentialAgent ---
# This agent orchestrates the pipeline by running the sub_agents in order.
Neo4j_information = SequentialAgent(
    name="Neo4j_information",
    sub_agents=[cve_info_fetcher_agent, cwe_info_fetcher_agent, capec_info_fetcher_agent, ttp_info_fetcher_agent, mitigation_plan_generator_agent, implementation_plan_generator_agent],
    description="Fetches information about CVE, CWE, CAPEC, and TTP, and generates a mitigation and implementation plan.",
    # The agents will run in the order provided: Writer -> Reviewer -> Refactorer
)

# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = Neo4j_information
