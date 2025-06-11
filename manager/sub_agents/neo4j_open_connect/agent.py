from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from neo4j import GraphDatabase

def open_and_connect_neo4j_browser(tool_context: object) -> dict:
    """Open the Neo4j browser and connect to the database."""
    print(f"--- Tool: open_and_connect_neo4j_browser called ---")
    
    # Open the Neo4j browser
    neo4j_browser_url = "http://localhost:7474"
    import webbrowser
    webbrowser.open(neo4j_browser_url)
    print(f"Neo4j browser opened at {neo4j_browser_url}")
    
    # Connect to the Neo4j instance
    neo4j_uri = "bolt://localhost:7687"
    neo4j_auth = ("neo4j", "neo4j")  # replace with your credentials
    driver = GraphDatabase.driver(neo4j_uri, auth=neo4j_auth)
    print(f"Connected to Neo4j instance at {neo4j_uri}")
    
    # Return the result
    return {
        "status": "success",
        "message": f"Neo4j browser opened at {neo4j_browser_url} and connected to instance at {neo4j_uri}",
    }

neo4j_open_connect=Agent(
    name="neo4j_open_connect",
    model="gemini-2.0-flash",
    description="An agent that opens the Neo4j browser and connects to the database.",
    instruction="""
    You are an agent that opens the Neo4j browser and connects to the database.
    
    When asked to open and connect:
    1. Open the Neo4j browser at the default URL (http://localhost:7474).
    2. Connect to the Neo4j instance using the provided credentials.
    
    Example response format:
    "Neo4j browser opened at <URL> and connected to instance at <URI>"
    """,
    tools=[open_and_connect_neo4j_browser]
)
