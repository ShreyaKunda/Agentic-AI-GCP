from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

def generate_match_query(entity: str, properties: dict, tool_context: ToolContext) -> dict:
    """Generate a MATCH query to view nodes based on specified properties."""
    print(f"--- Tool: generate_match_query called for entity: {entity}, properties: {properties} ---")
    
    # Start with the MATCH query template
    query = f"MATCH (n:{entity}) WHERE "
    
    # Add conditions based on provided properties
    query += " AND ".join([f"n.{key} = '{value}'" for key, value in properties.items()])
    query += " RETURN n"
    
    # Return the query
    return {"status": "success", "query": query, "entity": entity, "properties": properties}

# Create the Cypher query generating agent (only for MATCH action)
cypher_query_generator = Agent(
    name="cypher_query_generator",
    model="gemini-2.0-flash",
    description="An agent that generates MATCH Cypher queries to view nodes based on specific properties.",
    instruction=""" 
    You are an agent that generates Cypher MATCH queries to find nodes in a graph database.
    
    When asked to generate a Cypher query for viewing:
    1. Generate a MATCH query based on the provided entity and properties.
    2. The query will return the nodes that match the given conditions.
    
    Example response format:
    "Here is your Cypher query:
    <QUERY>"
    
    You will only support the 'match' action for this task.
    """,
    tools=[generate_match_query],
)
