from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from neo4j import GraphDatabase

def execute_cypher_query(query: str, tool_context: object) -> dict:
    """Execute a Cypher query in the Neo4j database and return the results."""
    print(f"--- Tool: execute_cypher_query called ---")
    
    # Connect to the Neo4j instance
    neo4j_uri = "bolt://localhost:7687"
    neo4j_auth = ("neo4j", "neo4j")  # replace with your credentials
    driver = GraphDatabase.driver(neo4j_uri, auth=neo4j_auth)
    print(f"Connected to Neo4j instance at {neo4j_uri}")
    
    # Execute the Cypher query
    with driver.session() as session:
        result = session.run(query)
        records = result.data()
        print(f"Executed Cypher query: {query}")
    
    # Return the results
    return {
        "status": "success",
        "message": f"Executed Cypher query: {query}",
        "results": records,
    }

cypher_query_executor = Agent(
    name="cypher_query_executor",
    model="gemini-2.0-flash",
    description="An agent that executes a Cypher query in a Neo4j database and returns the results.",
    instruction="""
    You are an agent that executes a Cypher query in a Neo4j database and returns the results.
    
    When asked to execute a Cypher query:
    1. Connect to the Neo4j instance using the provided credentials.
    2. Execute the Cypher query in the Neo4j database.
    3. Return the results of the query execution.
    
    Example response format:
    "Executed Cypher query: <QUERY> with results: <RESULTS>"
    """,
    tools=[execute_cypher_query]
)
