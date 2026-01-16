from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from modules.sqlalchemy_setup import get_db_session

from app.models.user_model import User
from app.models.message_model import Message
from fastapi.responses import JSONResponse
from modules.middleware import check_api_key

router = APIRouter(
  prefix="/chat",
  tags=["Chat"]
)

@router.post("/tes",dependencies=[Depends(check_api_key)])
def tes_chat() : 
    return JSONResponse(
        content=  { 
            "success" : True,
            "message": "Hello World"
        } 
    )

@router.post("/send")
def send_chat(
    payload: dict,
    db: Session = Depends(get_db_session)
):
    # return JSONResponse(
    #     content=  { 
    #         "success" : True,
    #         "message": "Hello World"
    #     }
    # )
    """
    payload contoh:
    {
      "baus_user_id": 123,
      "username": "divspan",
      "message": "tolong buatkan struk kopi"
    }
    """

    print("ENDPOINT TRIGGERRED")

    baus_user_id = payload["baus_user_id"]
    username = payload["username"]
    message_text = payload["message"]

    normalized_message = message_text.strip().lower()
    

    # 1️⃣ CEK / INSERT USER
    user = (
        db.query(User)
        .filter(User.baus_user_id == baus_user_id)
        .first()
    )

    if not user:
        user = User(
            baus_user_id=baus_user_id,
            username=username,
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 2️⃣ INSERT MESSAGE (USER)
    user_message = Message(
        # user_id=user.id,
        sender="human",
        raw_message=message_text
    )
    db.add(user_message)

    # 3️⃣ DUMMY AGENT RESPONSE
    if normalized_message == "!ping" : 
        agent_text = "pong"
    elif normalized_message == "!ping reply" : 
        agent_text = "pong reply"
    else :
        agent = "Struk sedang diproses 🧾✨ Silakan tunggu sebentar."
    # agent_text = "pong" if normalized_message == "!ping" else "Struk sedang diproses 🧾✨ Silakan tunggu sebentar."

    agent_message = Message(
        sender="agent",
        raw_message=agent_text
    )
    db.add(agent_message)

    db.commit()

    return JSONResponse(
        content={
            "success": True,
            "reply": agent_text
        }
    )
