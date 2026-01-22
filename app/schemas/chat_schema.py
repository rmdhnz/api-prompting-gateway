from pydantic import BaseModel

class ChatSendPayload(BaseModel):
    baus_user_id: int
    username: str
    message: str

class FallbackChatPayload(BaseModel) : 
    baus_user_id : int
    message : str