import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

AZURE_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_REGION = os.getenv("AZURE_SPEECH_REGION")

slides_file = "backend/output/data/slides.json"

with open(slides_file) as f:
    slides = json.load(f)

output_dir = "frontend/public/avatars"
os.makedirs(output_dir, exist_ok=True)

for slide in slides:
    text = slide["avatar_script"]
    slide_num = slide["slide_number"]

    url = f"https://{AZURE_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
        "User-Agent": "avatar-demo"
    }

    body = f"""
    <speak version='1.0' xml:lang='en-US'>
        <voice name='en-US-JennyNeural'>
            {text}
        </voice>
    </speak>
    """

    response = requests.post(url, headers=headers, data=body)

    output_file = f"{output_dir}/slide_{slide_num}.mp3"

    with open(output_file, "wb") as audio:
        audio.write(response.content)

    print(f"Generated voice for slide {slide_num}")