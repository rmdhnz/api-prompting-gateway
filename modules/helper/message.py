from datetime import datetime
from modules.messaging.rabbitmq import publish_babe_message
from app.models.message_model import Message
import os
from dotenv import load_dotenv
import requests
load_dotenv()
base_url = os.getenv("API_PROMPTING_URL")
api_key = os.getenv("BAUS_API_KEY")
def process_message(db, sender: str, raw_message: str):
    message = Message(
        sender=sender,
        raw_message=raw_message
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    # 2. Trigger rule
    if raw_message.strip().lower().startswith("!babe"):
        payload = {
            "type": "BAUS_AI_AGENT",
            "command": "!babe",
            "raw_message": raw_message,
            "metadata": {
                "message_id": message.id,
                "sender": sender,
                "received_at": datetime.utcnow().isoformat()
            }
        }

        publish_babe_message(payload)

    return message


def send_fallback(user_id: int, message: str) :
  url = f"{base_url}/chat/send-fallback"
  headers = {
    "x-api-key": api_key,
    "Content-Type": "application/json"
  }
  payload = {
    "baus_user_id" : user_id,
    "message": message
  }
  try :
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return True, response.json()
  except Exception as e :
    print(f"Error sending fallback: {e}")
    return None,None