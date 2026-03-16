import requests
import os
from dotenv import load_dotenv

load_dotenv()

AZURE_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_REGION = os.getenv("AZURE_SPEECH_REGION")

job_id = "test-slide-3"

url = f"https://{AZURE_REGION}.api.cognitive.microsoft.com/avatar/batchsyntheses/{job_id}?api-version=2024-08-01"

headers = {
    "Ocp-Apim-Subscription-Key": AZURE_KEY
}

response = requests.get(url, headers=headers)

print(response.json())