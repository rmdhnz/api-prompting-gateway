from sqlalchemy import String,Column,Integer,DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base) : 
  __tablename__ = "users"
  id = Column(Integer,primary_key=True,index=True)
  baus_user_id = Column(Integer,nullable=False,unique=True)
  username = Column(String,nullable=False,unique=True)
  role = Column(String,nullable=False)
  created_at = Column(DateTime,default=datetime.utcnow)
  updated_at = Column(datetime,default=datetime.utcnow,onupdate=datetime.utcnow)