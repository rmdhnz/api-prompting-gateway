from sqlalchemy import String,Column,Integer,DateTime
from datetime import datetime
from app.core.database import Base


class User(Base) : 
  __tablename__ = "users"
  id = Column(Integer,primary_key=True,index=True)
  baus_user_id = Column(Integer,nullable=False,unique=True)
  username = Column(String(255),nullable=False,unique=True)
  role = Column(String(100),nullable=False)
  created_at = Column(DateTime,default=datetime.utcnow)
  updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)