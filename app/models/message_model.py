from sqlalchemy import String,Column,Integer,DateTime,Enum
from datetime import datetime
from app.core.database import Base
class Message(Base) : 
  __tablename__ = "messages"
  id = Column(Integer,primary_key=True,index=True)
  sender = Column(
    Enum(
      "human",
      "agent",
      name="sender_enum"
    ),
    nullable=False,
    default="agent"
  )
  baus_user_id = Column(Integer,index=True,nullable=True)
  raw_message = Column(String(400),nullable=False)
  created_at = Column(DateTime,default=datetime.utcnow)
  updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)