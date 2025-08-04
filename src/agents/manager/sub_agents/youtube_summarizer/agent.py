from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from google.genai.client import Client

def transcribe_video(video_url: str, tool_context: ToolContext) -> dict:
    client = Client(api_key="Your API Key")

    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=types.Content(
            parts=[
                types.Part(
                    file_data=types.FileData(file_uri=video_url, mime_type='video/mp4')
                ),
                types.Part(text='Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions.')
            ]
        )
    )

    transcription = response.text

    # Extract key points from the transcription
    key_points = []
    for line in transcription.splitlines():
        if line.startswith("Timestamp:"):
            key_point = line.split(":", 1)[1].strip()
            key_points.append(key_point)

    # Create a summary of the transcription
    summary = "Summary of the video transcription:"
    for i, key_point in enumerate(key_points):
        summary += f"\n• {key_point}"

    return {"status": "success", "transcription": transcription, "summary": summary}
youtube_summarizer = Agent(
    name="youtube_summarizer",
    model="gemini-2.0-flash",
    description="Analyze a YouTube video by transcribing its content, detecting key moments, and generating a structured sand a detailed summary with timestamps.",
    instruction=(
        "Given a YouTube video URL:\n"
        "1. Transcribe the full audio content of the video accurately.\n"
        "2. Identify key moments and moments of interest in the video"
        "3. If the video is an explanation of a technical topic, provide a detailed summary of the content talked about in the video."
        "4. Provide what are the areas or topics to be learnt from the video and how the video can be used to learn them."
        "5. Explain technical jargon and provide definitions if needed."
    ),
    tools=[transcribe_video],
)
