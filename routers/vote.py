from fastapi import Depends, status, HTTPException, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import engine, get_db 
from fastapi.encoders import jsonable_encoder
import schema, model
from .jwttoken import get_current_user

router = APIRouter(prefix="/api/vote", tags=['VOTE'])


@router.post("/")
def election_cast(result: schema.Elect, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    vote_query = db.query(model.Voted).filter(model.Voted.auser_id == current_user.id).first()
    if vote_query != None:
        raise HTTPException(detail=f"Dear {current_user.fname} you have voted", status_code=status.HTTP_409_CONFLICT)
    else:
               
        new_vote = model.Voted(auser_id = current_user.id, candidate = result.candidate)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return "Successful Voting"

# @router.get("/result")
# def election_result(db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
#     # result_query = Session.query(model.Voted.voted, func.count(model.Voted.candidate)).group_by(model.Voted.candidate).all()
#     result = db.query(func.count(model.Voted.candidate)).group_by(model.Voted.auser_id)
#     json_compatible_item_data = jsonable_encoder(result)
#     print(json_compatible_item_data)
#     return json_compatible_item_data






# @router.post("/", status_code=status.HTTP_201_CREATED)
# def votes(vote: schema.Votes, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
#     vote_query = db.query(model.Vote).filter(
#         model.Vote.auser_id == vote.auser_id, model.Vote.user_id == current_user.id)
#     tranx_vote = db.query(model.TranxGLDb).filter(model.TranxGLDb.id == vote.auser_id).first()
#     if not tranx_vote:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Transaction with ID {vote.auser_id} not found")
#     found_vote = vote_query.first()
#     if (vote.dir == 1):
#         if found_vote:
#             raise HTTPException(detail=f"{current_user.id} has already voted", 
#                             status_code=status.HTTP_409_CONFLICT)
#         new_vote = model.Vote(user_id = current_user.id, auser_id = vote.auser_id)
#         db.add(new_vote)
#         db.commit()
#         db.refresh(new_vote)
#         return "Successful Voting"
#     elif (vote.dir == 0):
#         vote_delete = db.query(model.Vote).filter(model.Vote.auser_id == vote.auser_id)
#         if not vote_delete.first():
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"{current_user.id} cannot Vote")
#         vote_delete.delete(synchronize_session=False)
#         db.commit()
#         return "Sucessfully Deleted"  