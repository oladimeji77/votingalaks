from fastapi import Depends, status, HTTPException, Response, APIRouter
from typing import List
from hash import hasher
from sqlalchemy.orm import Session
from database import engine, get_db 
import schema, model
from .jwttoken import get_current_user

router = APIRouter(prefix="/api/tranx", tags=['Transactions'])


@router.get("/", response_model=List[schema.TranxGLDb])
def tranxhistory(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    check_user = db.query(model.TranxGLDb).filter(model.TranxGLDb.user_id == current_user.id)
    if check_user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not allowed to perform the operation")
    all_tranx = check_user.all()
    print(current_user.id)
    return all_tranx

@router.get("/{tranx_id}")
def tranxhistory(tranx_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    check_tranx = db.query(model.TranxGLDb).filter(model.TranxGLDb.id == tranx_id).first()
    if not check_tranx:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"transaction with id: {tranx_id} not found")
    if check_tranx.user_id is not current_user.id:
        raise HTTPException(detail=f"Transaction not found", status_code=status.HTTP_404_NOT_FOUND)
    return check_tranx

@router.post("/", status_code=status.HTTP_201_CREATED)
def new_tranx(request: schema.TranxGLDb, db: Session = Depends(get_db), current_user: schema.TranxGLDb = Depends(get_current_user)):
    new_tranx = model.TranxGLDb(user_id = current_user.id, **request.dict())
    db.add(new_tranx)
    db.commit()
    db.refresh(new_tranx)
    return new_tranx

@router.put("/{tranx_id}")
def update_tranx(tranx_id: int, new_entry: schema.TranxGLDb, db: Session = Depends(get_db), current_user: schema.TranxGLDb = Depends(get_current_user)):
    check_user = db.query(model.TranxGLDb).filter(model.TranxGLDb.user_id == current_user.id)
    if check_user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not allowed to perform the operation")
    updated_tranx = db.query(model.TranxGLDb).filter(model.TranxGLDb.id == tranx_id)
    if updated_tranx.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    new_tranx = updated_tranx.update(new_entry.dict(), synchronize_session=False)
    db.commit()
    new_tranx = updated_tranx.first()
    return new_tranx

@router.delete("/{tranx_id}")
def delete_tranx(tranx_id: int, db: Session = Depends(get_db), current_user: schema.TranxGLDb = Depends(get_current_user)):
    print(current_user.fname)
    check_user = db.query(model.TranxGLDb).filter(model.TranxGLDb.user_id == current_user.id)
    if check_user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You are not the owner")
    tranx2del = db.query(model.TranxGLDb).filter(model.TranxGLDb.id == tranx_id)
    if not tranx2del.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not allowed to perform the operation")
    tranx2del.delete(synchronize_session=False)
    db.commit()
    return "Sucessfully Deleted"



