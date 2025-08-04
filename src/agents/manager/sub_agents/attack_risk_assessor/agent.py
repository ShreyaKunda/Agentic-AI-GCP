from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from manager.sub_agents.threat_generator.agent import threat_generator

attack_risk_assessor = Agent(
    name="attack_risk_assessor",
    model="gemini-2.0-flash",
    description="Analyzes threat chains for criticality, future risk, and provides prevention steps.",
    instruction="""
    When given a threat path, use the threat_generator tool to get threat chains.
    Then, analyze the chains for criticality, future risk, and prevention steps.
    Present your analysis in a structured format.
    """,
    tools=[AgentTool(threat_generator)],
)