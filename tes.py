import requests
import os
from dotenv import load_dotenv

load_dotenv()



API_URL = "http://31.97.106.30:3003/chat/send"
API_KEY = os.getenv("BAUS_API_KEY")

payload = {
    "baus_user_id": 23,
    "username": "baus-dev",
    "message": "Hello From Script 🚀",
}

res = requests.post(
    API_URL,
    json=payload,
    headers={
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
    },
)

print(res.json())
