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
from manager.sub_agents.threat_generator.agent import threat_generator
from manager.sub_agents.attack_risk_assessor.agent import attack_risk_assessor
from manager.sub_agents.threat_chain_visualizer.agent import threat_chain_visualizer
from manager.sub_agents.incident_response_agent.agent import incident_response_agent
from manager.sub_agents.threat_intelligence_aggregator.agent import threat_intelligence_aggregator

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Central manager agent for delegating and orchestrating security automation tasks. ",
    instruction="""
    You are a Manager Agent, responsible for coordinating and delegating tasks to specialized agents within a security automation system. Your primary function is to efficiently handle user requests by directing them to the appropriate specialized agent based on the task.

The below is your Operational Workflow:
1. Initialization
    Upon startup, display the following message:
    “I am responsible for coordinating and delegating tasks to specialized agents. Describe what you want to do.

2. Wait for Input
    After displaying the message, wait for user input.

3. Accepting Requests
    Accept user requests in one of two formats: By typing the corresponding option number (1 to 13), or by providing a detailed description of the request.

4. Delegating Tasks
    Based on the user input, delegate the task to the most suitable agent from the following list:
    a. cypher_query_generator: Generates Cypher queries for Neo4j databases.
    b. log_summarizer: Summarizes threat logs for rapid analysis.
    c. neo4j_open_connect: Connects and interacts with the Neo4j database.
    d. article_summarizer: Summarizes YouTube videos for threat intelligence or training.
    e. youtube_summarizer: Summarizes YouTube videos.
    f. image_summarizer: Summarizes and interprets images relevant to security.
    g. flame_graph_summarizer: Analyzes and summarizes flame graphs for performance or threat analysis.
    h. cypher_query_executor: Executes Cypher queries.
    i. threat_generator: Generates detailed threat chains from attack paths.
    j. attack_risk_assessor: Assesses the risk and criticality of threat chains; provides prevention steps.
    k. threat_chain_visualizer: Visualizes threat chains as diagrams or graphs.
    l. incident_response_agent: Suggests and automates incident response actions based on threat chains and risk.
    m. threat_intelligence_aggregator: Aggregates and correlates the latest threat intelligence with existing threat chains.
    n. mitigation_finder: (Special case) Identifies appropriate mitigation strategies for threat response.


Mitigation Handling
If the user request involves mitigation, use the tool:
mitigation_finder.


    """,
    sub_agents=[
        cypher_query_generator,
        log_summarizer,
        neo4j_open_connect,
        article_summarizer,
        youtube_summarizer,
        image_summarizer,
        flame_graph_summarizer,
        cypher_query_executor,
        threat_generator,
        attack_risk_assessor,
        threat_chain_visualizer,
        incident_response_agent,
        threat_intelligence_aggregator,
    ],
    tools=[
        AgentTool(mitigation_finder),
    ],
)

def aggregate_agent_outputs(input_data):
    outputs = {}
    for agent in root_agent.sub_agents:
        try:
            outputs[agent.name] = agent.run(input_data)
        except Exception as e:
            outputs[agent.name] = f"Error: {e}"
    return outputs

if __name__ == "__main__":
    root_agent.run()
