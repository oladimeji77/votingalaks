from sqlalchemy import Column, Integer,String, Boolean, ForeignKey
from database import Base
from datetime import datetime
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import Relationship

class AccreditedUserDB(Base):
    __tablename__ = "ausers"
    id = Column(Integer, primary_key=True, index=True)
    fname = Column(String, nullable=False)
    lname = Column(String, nullable=False)
    username = Column(String, nullable=False)
    Email = Column(String, nullable=False)
    Password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())
    #transactions =  relationship("TranxGLDb", back_populates='user')
 

# class TranxGLDb(Base):
#     __tablename__ = "tranx"
#     id = Column(Integer, primary_key=True, index=True)
#     amount = Column(Integer)
#     currency = Column(String, default='NGN')
#     payout = Column(Integer)
#     Success = Column(Boolean, default=False)
#     created_at = Column(TIMESTAMP, default=datetime.now()) 
#     user_id = Column(Integer, ForeignKey('NewUser.id', ondelete="CASCADE"), nullable=False)
#     user =  Relationship("UserDB")

# class Vote(Base):
#     __tablename__ = "votes"
#     auser_id = Column(Integer, ForeignKey("auser.id", ondelete="CASCADE"), primary_key=True)
#     vote_id = Column(Integer, ForeignKey("tranx.id", ondelete="CASCADE"), primary_key=True)
    


    
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
    
    
