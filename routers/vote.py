from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from database import engine, get_db 
import schema, model
from .jwttoken import get_current_user

router = APIRouter(prefix="/api/vote", tags=['VOTE'])


@router.post("/", status_code=status.HTTP_201_CREATED)
def votes(vote: schema.Votes, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    vote_query = db.query(model.Vote).filter(
        model.Vote.tranx_id == vote.tranx_id, model.Vote.user_id == current_user.id)
    tranx_vote = db.query(model.TranxGLDb).filter(model.TranxGLDb.id == vote.tranx_id).first()
    if not tranx_vote:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with ID {vote.tranx_id} not found")
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(detail=f"{current_user.id} has already voted", 
                            status_code=status.HTTP_409_CONFLICT)
        new_vote = model.Vote(user_id = current_user.id, tranx_id = vote.tranx_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return "Successful Voting"
    elif (vote.dir == 0):
        vote_delete = db.query(model.Vote).filter(model.Vote.tranx_id == vote.tranx_id)
        if not vote_delete.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{current_user.id} cannot Vote")
        vote_delete.delete(synchronize_session=False)
        db.commit()
        return "Sucessfully Deleted"


        