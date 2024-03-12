from fastapi import FastAPI, Depends, status, HTTPException, Response, APIRouter
from typing import Optional, List
from hash import hasher
from sqlalchemy.orm import Session
from database import engine, get_db 
import schema, model
from .jwttoken import get_current_user

router = APIRouter(prefix="/api/users", tags=['Users'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.CreateUserRes)
def create_user(request: schema.CreateUser, db: Session = Depends(get_db)):
    hashed_password = hasher(request.Password)
    request.Password = hashed_password
    new_user = model.AccreditedUserDB(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=schema.SpecificUser)
def specific_users(user_id: int, db: Session = Depends(get_db), current_user: schema.TranxGLDb = Depends(get_current_user)):
    single_user = db.query(model.AccreditedUserDB).filter(model.AccreditedUserDB.id == user_id).first()
    if single_user == None:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail=f"User with id: {user_id} is not here")
    return single_user

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schema.CreateUserRes])
def all_users(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    print(current_user.fname)
    all_user = db.query(model.AccreditedUserDB).all()
    return all_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    todelete = db.query(model.AccreditedUserDB).filter(model.AccreditedUserDB.id == user_id)
    if not todelete.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} not found")
    todelete.delete(synchronize_session=False)
    db.commit()
    return "Sucessfully Deleted"

@router.put("/{user_id}")
def update_user(user_id, request: schema.UpdateUser, db: Session = Depends(get_db), current_user: schema.TranxGLDb = Depends(get_current_user)):
    updated_user = db.query(model.UserDB).filter(model.AccreditedUserDB.id == user_id)
    if not updated_user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {user_id} not found")
    updated_user.update(request.dict(), synchronize_session=False)
    db.commit()
    updated_user = updated_user.first()
    return updated_user
