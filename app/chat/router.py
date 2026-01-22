from fastapi import APIRouter, Depends,Query
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.models.message_model import Message
from modules.sqlalchemy_setup import get_db_session
from modules.middleware import check_api_key
from app.core.ws_manager import manager
from app.schemas.chat_schema import ChatSendPayload,FallbackChatPayload
from app.controllers.chat_controller import *


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

@router.get("/history")
def chat_history(
    baus_user_id: int = Query(...),
    db: Session = Depends(get_db_session),
):
    return {
        "success": True,
        "messages": fetch_history(db, baus_user_id),
    }


@router.post("/send-fallback", dependencies=[Depends(check_api_key)])
async def send_chat_fallback(
    payload: FallbackChatPayload,
    db: Session = Depends(get_db_session),
):
    # reply = generate_agent_reply(payload.message)

    await save_agent_message(
        db=db,
        baus_user_id=payload.baus_user_id,
        agent_text=payload.message,
    )

    return JSONResponse(
        content={
            "success": True,
            "reply": payload.message,
        }
    )



@router.post("/tes", dependencies=[Depends(check_api_key)])
def tes_chat():
    return JSONResponse(
        content={
            "success": True,
            "message": "Hello World",
        }
    )


@router.post("/send", dependencies=[Depends(check_api_key)])
async def send_chat(
    payload: ChatSendPayload,
    db: Session = Depends(get_db_session),
):
    reply = await handle_send_chat(payload, db)

    return JSONResponse(
        content={
            "success": True,
            "reply": reply,
        }
    )




# @router.post("/send")
# async def send_chat_ws(payload: ChatSendPayload,db: Session = Depends(get_db_session)):
#     # db = SessionLocal()
#     try:
#         # 1. save user message
#         user_msg = Message(
#             sender="human",
#             raw_message=payload.message,
#             baus_user_id=payload.baus_user_id,
#         )
#         db.add(user_msg)
#         db.commit()

#         # await manager.send_to_user(
#         #     payload.baus_user_id,
#         #     {
#         #         "sender": "human",
#         #         "content": payload.message,
#         #     }
#         # )

#         reply_text = generate_agent_reply(payload.message)

#         agent_msg = Message(
#             sender="agent",
#             raw_message=reply_text,
#             baus_user_id=payload.baus_user_id,
#         )
#         db.add(agent_msg)
#         db.commit()

#         await manager.send_to_user(
#             payload.baus_user_id,
#             {
#                 "sender": "agent",
#                 "content": reply_text,
#             }
#         )

#         return {"success": True}

#     finally:
#         db.close()
