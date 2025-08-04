from google.genai import types
from google.genai.client import Client

client = Client(api_key="AIzaSyDWJ-4pN-hZpoA2KBqtmMMu-Q6h1WEFjuo")

response = client.models.generate_content(
    model='models/gemini-2.0-flash',
    contents=types.Content(
        parts=[
            types.Part(
                file_data=types.FileData(file_uri='https://www.youtube.com/watch?v=9hE5-98ZeCg', mime_type='video/mp4')
            ),
            types.Part(text='Transcribe the audio from this video, giving timestamps for salient events in the video. Also provide visual descriptions.')
        ]
    )
)

print(response.text)
