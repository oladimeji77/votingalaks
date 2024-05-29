from fastapi import FastAPI, Depends, status, HTTPException, Response, APIRouter, BackgroundTasks
from typing import Optional, List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from hash import hasher
from starlette.responses import JSONResponse
from config import settings as ss
from sqlalchemy.orm import Session
from database import engine, get_db 
import schema, model
from .jwttoken import get_current_user

router = APIRouter(prefix="/api/users", tags=['USERS'])

conf = ConnectionConfig(
    MAIL_USERNAME = ss.MAIL_USERNAME,
    MAIL_PASSWORD = ss.MAIL_PASSWORD,
    MAIL_FROM = ss.MAIL_FROM,
    MAIL_PORT = ss.MAIL_PORT,
    MAIL_SERVER = ss.MAIL_SERVER,
    MAIL_FROM_NAME=ss.MAIL_FROM_NAME,
    MAIL_STARTTLS = ss.MAIL_STARTTLS,
    MAIL_SSL_TLS = ss.MAIL_SSL_TLS,
    USE_CREDENTIALS = ss.USE_CREDENTIALS,
    VALIDATE_CERTS = ss.VALIDATE_CERTS
)



# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.CreateUserRes)
# def create_user(request: schema.CreateUser, db: Session = Depends(get_db)):
#     hashed_password = hasher(request.Password)
#     request.Password = hashed_password
#     new_user = model.AccreditedUserDB(**request.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.CreateUserRes)
def create_user(background_tasks: BackgroundTasks, request: schema.CreateUser, db: Session = Depends(get_db)):
    check_email = db.query(model.AccreditedUserDB).filter(model.AccreditedUserDB.Email == request.Email).first()
    print(check_email)
    print(list(request.Email.split(" ")) )
    print(request.dict().get("email"))
    if check_email != None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Email has already been used")
    check_username = db.query(model.AccreditedUserDB).filter(model.AccreditedUserDB.username == request.username).first()
    if check_username != None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Username has been taken")
    # check_phone = db.query(model.AccreditedUserDB).filter(model.AccreditedUserDB.phone_number == request.phone_number).first()
    # if check_phone != None:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Phone number exist in our records")
    hashed_password = hasher(request.Password)
    request.Password = hashed_password
    new_user = model.AccreditedUserDB(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    
    #Email functinality
    html = f"""<html>
        <body style="margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, Helvetica, sans-serif;">
        <div style="width: 100%; background: #efefef; border-radius: 10px; padding: 10px;">
        <div style="margin: 0 auto; width: 90%; text-align: center;">
            <h1 style="background-color: rgba(0, 53, 102, 1); padding: 5px 10px; border-radius: 5px; color: white;"> Welcome to Alaka Voting Portal </h1>
            <div style="margin: 30px auto; background: white; width: 40%; border-radius: 10px; padding: 50px; text-align: center;">
            <h3 style="margin-bottom: 100px; font-size: 24px;"> Dear { request.fname }!</h3>
            <p style="margin-bottom: 30px;">We're thrilled to welcome you to Alaks Portal! We're excited to have you, please note that
             your vote is secured and please shun election malpractice..</p>
            <a style="display: block; margin: 0 auto; border: none; background-color: rgba(255, 214, 10, 1); color: white; width: 200px; line-height: 24px; padding: 10px; font-size: 24px; border-radius: 10px; cursor: pointer; text-decoration: none;"
                href="http://172.210.76.243/result" target="_blank">
                Let's Go
            </a></div></div></div></body></html> /p>"""
    message = MessageSchema(
        subject="Welcome to Alaks Voting Portal",
        recipients=list(request.Email.split(" ")),
        body=html,
        cc = ["oladimeji.oladepo@gmail.com"],
        subtype=MessageType.html)

    fm = FastMail(conf)

    background_tasks.add_task(fm.send_message, message, template_name='email.html')


    return JSONResponse(status_code=200, content={"message": "Confirmation email has been sent to your mail"})
    #return new_user

@router.get("/me")
def get_me(user: schema.SpecificUser = Depends(get_current_user)):
    return user

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



