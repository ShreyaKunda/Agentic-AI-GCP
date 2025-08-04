from google.adk.agents import Agent

incident_response_agent = Agent(
    name="incident_response_agent",
    model="gemini-2.0-flash",
    description="Suggests and automates incident response actions based on risk assessment and threat chains.",
    instruction="""
    When given a threat chain and risk assessment, analyze the situation and recommend incident response actions.
    If the risk is high or severe, suggest automated containment or remediation steps.
    Provide a clear, step-by-step incident response plan tailored to the threat chain and its impact.
    """,
    tools=[],
)