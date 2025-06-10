from google.adk.agents import Agent
from google.adk.tools import google_search

# Define the mitigation finder agent
mitigation_finder = Agent(
    name="mitigation_finder",
    model="gemini-2.0-flash",
    description="Cyber threat mitigation finder agent",
    instruction=""" 
    You are an assistant that helps find mitigations for various cyber threats with a summary of the an atttack and the logs.
    
    When a cyber threat is provided:
    1. Use the `google_search` tool to search for mitigation strategies and solutions.
    2. Look for credible sources, articles, and best practices related to mitigating the identified threat.
    3. Provide a summary of the findings, including recommended actions or resources for mitigation in a detailed manner without being vague or overly simplistic.
    4. Provide a step-by-step guide on how to implement the mitigation strategies and solutions.
    5. Provide a clear and concise explanation of the steps required to implement the mitigation strategies and solutions.
    You should tailor the search to match the specific cyber threat identified.
    """,
    tools=[google_search],
)

# Example of how the agent might be used:
# For instance, if the agent receives a request to find mitigations for "ransomware", it would search for relevant mitigation techniques.
