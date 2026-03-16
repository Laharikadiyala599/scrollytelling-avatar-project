from pathlib import Path
import json
import os
import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

SLIDES_JSON = BASE_DIR / "output" / "data" / "slides.json"
OUTPUT_DIR = BASE_DIR / "output" / "avatars"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

API_VERSION = "2024-08-01"


def load_slide_script(slide_index):
    with open(SLIDES_JSON, "r", encoding="utf-8") as f:
        slides = json.load(f)

    slide = slides[slide_index]
    return slide["avatar_script"]


def create_batch_avatar_job(text):
    endpoint = f"https://{AZURE_SPEECH_REGION}.api.cognitive.microsoft.com"
    url = f"{endpoint}/avatar/batchsyntheses/test-slide-3?api-version={API_VERSION}"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY,
        "Content-Type": "application/json",
    }

    payload = {
        "inputKind": "plainText",
        "inputs": [
            {
                "content": text
            }
        ],
        "synthesisConfig": {
            "voice": "en-US-JennyNeural"
        },
        "avatarConfig": {
            "customized": False,
            "talkingAvatarCharacter": "lisa",
            "talkingAvatarStyle": "casual-sitting",
            "videoFormat": "webm",
            "videoCodec": "vp9",
            "backgroundColor": "#00000000"
        }
    }

    response = requests.put(url, headers=headers, json=payload, timeout=60)
    print("Status code:", response.status_code)
    print(response.text)

    response.raise_for_status()
    return response.json()


def main():
    if not AZURE_SPEECH_KEY or not AZURE_SPEECH_REGION:
        raise ValueError("Missing AZURE_SPEECH_KEY or AZURE_SPEECH_REGION in .env")

    script_text = load_slide_script(2)
    result = create_batch_avatar_job(script_text)

    output_file = OUTPUT_DIR / "avatar_slide_3_job.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Saved job response to: {output_file}")


if __name__ == "__main__":
    main()