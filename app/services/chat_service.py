from sqlalchemy.orm import Session
from app.models.message_model import Message
# from modules.sqlalchemy_setup import get
from app.core.database import SessionLocal
from app.core.ws_manager import manager
import os
import requests
from dotenv import load_dotenv
import asyncio
load_dotenv()
async def save_user_message(
    db: Session,
    baus_user_id: int,
    message_text: str,
):
    message = Message(
        sender="human",
        raw_message=message_text,
        baus_user_id=baus_user_id,
    )
    db.add(message)
    await manager.send_to_user(
        baus_user_id,
        {
            "sender" : "human",
            "content" : message_text,
        }
    )
    return message


def generate_agent_reply(message_text: str) -> str:
    normalized = message_text.strip().lower()

    if normalized == "!ping":
        return "pong"
    elif normalized == "!ping reply":
        return "pong reply"

    return "Apaan Sih..."


async def save_agent_message(
    db: Session,
    agent_text: str,
    baus_user_id: int | None = None
):
    message = Message(
        sender="agent",
        raw_message=agent_text,
        baus_user_id=baus_user_id
    )
    db.add(message)
    await manager.send_to_user(
        baus_user_id,
        {
            "sender" : "agent",
            "message" : agent_text
        }
    )
    return message

# def reply_direct_message(
#     db: Session,
#     message: str,
#     baus_user_id: int | None = None,
# ) -> None:

#     user_message = Message(
#         sender="human",
#         raw_message=message,
#         baus_user_id=baus_user_id,
#     )
#     db.add(user_message)

#     reply_text = message

#     agent_message = Message(
#         sender="agent",
#         raw_message=reply_text,
#         baus_user_id=baus_user_id,
#     )
#     db.add(agent_message)

#     db.commit()

def reply_direct_message_with_db(
    db: Session,
    message: str,
    baus_user_id: int,
):
    # save human
    # user_msg = Message(
    #     sender="human",
    #     raw_message=message,
    #     baus_user_id=baus_user_id,
    # )
    # db.add(user_msg)

    # agent reply
    agent_msg = Message(
        sender="agent",
        raw_message=message,
        baus_user_id=baus_user_id,
    )
    db.add(agent_msg)

    db.commit()

    # 🔥 PUSH KE WS (ASYNC)
    safe_send_ws(
        baus_user_id,
        {
            "sender": "agent",
            "content": message,
        }
    )
    # print("Berhasi")

def reply_direct_message(
    message: str,
    baus_user_id: int | None = None
) -> None:
    """
    Helper function (tanpa db param)
    Cocok untuk CLI / worker / testing
    """
    db = SessionLocal()
    try:
        reply_direct_message_with_db(db, message,baus_user_id)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def get_chat_history(
    db: Session,
    baus_user_id: int,
):
    return (
        db.query(Message)
        .filter(Message.baus_user_id == baus_user_id)
        .order_by(Message.id.asc())
        .all()
    )

def safe_send_ws(baus_user_id: int, payload: dict):
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        loop.create_task(manager.send_to_user(baus_user_id, payload))
    else:
        asyncio.run(manager.send_to_user(baus_user_id, payload))


base_url = os.getenv("API_PROMPTING_URL")
api_key = os.getenv("BAUS_API_KEY")

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
