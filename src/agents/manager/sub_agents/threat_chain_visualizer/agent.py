from google.adk.agents import Agent

threat_chain_visualizer = Agent(
    name="threat_chain_visualizer",
    model="gemini-2.0-flash",
    description="Visualizes threat chains as diagrams or graphs for easier analysis.",
    instruction="""
    When given a threat chain, convert it into a visual diagram or graph.
    Present the visualization in a format suitable for security professionals.
    """,
    tools=[],
)