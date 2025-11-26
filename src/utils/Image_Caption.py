from google.genai import types
from google.genai.client import Client

# Create a client instance
client = Client(api_key="Your API Key")

# Load the image file
with open('/home/administrator/workspace/Shreya/Agentic_AI/Agentic_AI/sample.png', 'rb') as f:
    image_bytes = f.read()

# Generate a caption for the image
response = client.models.generate_content(
    model='gemini-2.0-flash',
    contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type='image/png',  # Update the mime type to 'image/png'
        ),
        'Caption this image.'
    ]
)

# Print the generated caption
print(response.text)
