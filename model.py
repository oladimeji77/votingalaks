from sqlalchemy import Column, Integer,String, Boolean, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class AccreditedUserDB(Base):
    __tablename__ = "ausers"
    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String, nullable=False)
    lname = Column(String, nullable=False)
    username = Column(String, nullable=False)
    Email = Column(String, nullable=False)
    Password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())
   
 

class Voted(Base):
    __tablename__ = "voted"
    auser_id = Column(Integer, ForeignKey("ausers.id", ondelete="CASCADE"), primary_key=True, unique=True)
    candidate = Column(String, nullable=False)
    


    
# class Blog(Base):
#     __tablename__ = "blog"
#     id = Column(Integer, primary_key=True, nullable=False)
#     title = Column(String, nullable=False)
#     content = Column(String, nullable=False)
#     published = Column(Boolean, server_default='True', nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')
#     owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     owner = Relationship("User")
    


# class User(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True, nullable=False)
#     email = Column(String, nullable=False, unique=True)
#     password = Column(String, nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default='now()')
    
    
