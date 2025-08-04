from google.adk.agents import Agent
from google.adk.tools import google_search

image_summarizer = Agent(
    name="image_summarizer",
    model="gemini-2.0-flash",
    description="Image Summarizer for given image",
    instruction="""Generate an image summary for the given image in 5-10 sentences.""",
    tools=[],
)
