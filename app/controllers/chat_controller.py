from sqlalchemy.orm import Session

from app.schemas.chat_schema import ChatSendPayload
from app.services.user_service import get_or_create_user
from app.services.chat_service import (
    save_user_message,
    save_agent_message,
    generate_agent_reply,
    get_chat_history
)
from modules.messaging.rabbitmq import publish_babe_message

from app.core.ws_manager import manager


def fetch_history(db: Session, baus_user_id: int):
    messages = get_chat_history(db, baus_user_id)

    return [
        {
            "id": m.id,
            "sender": m.sender,
            "message": m.raw_message,
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ]


async def handle_send_chat(
    payload: ChatSendPayload,
    db: Session,
):
    # 1. user
    user = get_or_create_user(
        db=db,
        baus_user_id=payload.baus_user_id,
        username=payload.username,
    )

    # 2. save user message
    await save_user_message(
        db=db,
        baus_user_id=payload.baus_user_id,
        message_text=payload.message,
    )

    message = payload.message.strip()

    if message.lower().startswith("!babe") : 
        print("Publish message to BABE via RABBITMQ")
        publish_babe_message({
            "baus_user_id" : payload.baus_user_id,
            "username" : payload.username,
            "raw_message" : message,
            "source" : "chat"
        })

        agent_text = "✅ Perintah diterima, sedang diproses AI Agent"
        await save_agent_message(
            db=db,
            agent_text=agent_text,
            baus_user_id=payload.baus_user_id
        )
        db.commit()
        return agent_text


    # 3. agent logic
    agent_text = generate_agent_reply(payload.message)

    # 4. save agent message
    await save_agent_message(
        db=db,
        agent_text=agent_text,
        baus_user_id=payload.baus_user_id,
    )

    db.commit()

    # await manager.send_to_user(
    #     payload.baus_user_id,
    #     {
    #         "sender" : "agent",

    #     }
    # )

    return agent_text


def send_fallback(
        payload: ChatSendPayload,
        db: Session,
) : 
    agent_text = "Maaf, terjadi kesalahan pada sistem. Silakan coba lagi nanti."

    message = save_agent_message(
        db=db,
        agent_text=agent_text,
        baus_user_id=payload.baus_user_id,
    )

    db.commit()

    return message