from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from manager.sub_agents.cypher_query_generator.agent import cypher_query_generator
from manager.sub_agents.log_summarizer.agent import log_summarizer
from manager.sub_agents.neo4j_open_connect.agent import neo4j_open_connect
from manager.sub_agents.mitigation_finder.agent import mitigation_finder
from manager.sub_agents.article_summarizer.agent import article_summarizer
from manager.sub_agents.youtube_summarizer.agent import youtube_summarizer
from manager.sub_agents.image_summarizer.agent import image_summarizer
from manager.sub_agents.flame_graph_summarizer.agent import flame_graph_summarizer
from manager.sub_agents.cypher_query_executor.agent import cypher_query_executor
root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="""
    You are a manager agent that is responsible for overseeing the work of the other agents. The first task that you have to perform is display the below text in a proper manner.
     Welcome to the Manager Agent!
    I can help you with the following tasks:
    1. Generate Cypher queries
    2. Summarize Threat Logs
    3. Connect to Neo4j database and open your Neo4j Database
    4. Find mitigations for threats
    5. Summarize YouTube Videos.
    6. Summarize and help understand images.
    7. Analyze and summarize flame graphs.
    Please select an option by typing the corresponding option.

    Always delegate the task to the appropriate agent. Use your best judgement 
    to determine which agent to delegate to.

    You are responsible for delegating tasks to the following agent:
    - cypher_query_generator
    - log_summarizer
    - neo4j_open_connect
    - neo4j_query_agent
    - article_summarizer
    - youtube_summarizer
    - image_summarizer
    - flame_graph_summarizer
    - cypher_query_executor
    - 

   
    You also have access to the following tools:
    
    - mitigation_finder
    """,
    sub_agents=[cypher_query_generator, log_summarizer,neo4j_open_connect,article_summarizer, youtube_summarizer, image_summarizer, flame_graph_summarizer, cypher_query_executor],
    tools=[
        AgentTool(mitigation_finder),
    ],
)

if __name__ == "__main__":
    root_agent.run()
