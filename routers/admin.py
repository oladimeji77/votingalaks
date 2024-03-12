from fastapi import FastAPI, Depends, status, HTTPException, Response, APIRouter
from typing import Optional, List
from hash import hasher
from sqlalchemy.orm import Session
from database import engine, get_db 
import schema, model
from .jwttoken import get_current_user

router = APIRouter(prefix="/api/super-admin", tags=['Administrator'])



@router.get("/", status_code=status.HTTP_200_OK)
def all_users(db: Session = Depends(get_db)):
    all_user = db.query(model.UserDB).all()
    return all_user

@router.get("/tranx", status_code=status.HTTP_200_OK)
def all_tranx(db: Session = Depends(get_db)):
    all_user = db.query(model.TranxGLDb).all()
    return all_user



@router.put("/{user_id}")
def update_user(user_id, request: schema.UpdateUser, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    #updated_user = db.query(model.UserDB).filter(model.UserDB.id == user_id).update(request)
    updated_user = db.query(model.UserDB).filter(model.UserDB.id == user_id)
    if not updated_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} not found")
    updated_user.update(request.dict(), synchronize_session=False)
    db.commit()
    updated_user = updated_user.first()
    return updated_user


@router.put("/{tranx_id}")
def update_user(tranx_id, request: schema.UpdateUser, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    #updated_user = db.query(model.UserDB).filter(model.UserDB.id == user_id).update(request)
    updated_user = db.query(model.TranxGLDb).filter(model.TranxGLDb.id == tranx_id)
    if not updated_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} not found")
    updated_user.update(request.dict(), synchronize_session=False)
    db.commit()
    updated_user = updated_user.first()
    return updated_user
