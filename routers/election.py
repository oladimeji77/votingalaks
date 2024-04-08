from fastapi import FastAPI, Depends, status, HTTPException, Response, APIRouter
from typing import Optional, List
from hash import hasher
from sqlalchemy.orm import Session
from database import engine, get_db 
import schema, model
from .jwttoken import get_current_user

router = APIRouter(prefix="/api/elects", tags=['ELECT'])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.ElectRes)
def create_elect(request: schema.Elect, db: Session = Depends(get_db), current_election: int = Depends(get_current_user)):
    request.user_id = current_election.id
    new_election = model.ElectionDb(**request.dict())
    db.add(new_election)
    db.commit()
    db.refresh(new_election)
    return new_election






