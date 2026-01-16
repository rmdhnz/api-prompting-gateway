from sqlalchemy import String,Column,Integer,DateTime,Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

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
  raw_message = Column(String,nullable=False,unique=True)
  created_at = Column(DateTime,default=datetime.utcnow)
  updated_at = Column(datetime,default=datetime.utcnow,onupdate=datetime.utcnow)