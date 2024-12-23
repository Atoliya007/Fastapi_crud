from sqlalchemy import Boolean, Column ,Integer,String,DateTime,func
from database import Base
from sqlalchemy import *

# from datetime import datetime
# import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True, index=True)
    username = Column(String(50),unique=True)

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer,primary_key=True, index=True)

    title = Column(String(50))
    content = Column(String(100))
    user_id = Column(Integer)
    name = Column(String(30))
    email = Column(String(50))
    age = Column(Integer)
    gender = Column(String(10), nullable=False)
    is_active = Column(Boolean)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)

    