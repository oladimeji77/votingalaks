from pydantic import BaseModel, EmailStr
from typing import Annotated, Union
from datetime import datetime
from typing import Optional
from pydantic.types import conint
from pydantic import ConfigDict

################################################################################
##############################  Registration   #################################

class CreateUser(BaseModel):
    fname: str
    lname: str
    username: str
    Email: EmailStr
    Password: str

class CreateUserRes(BaseModel):
    fname: str
    lname: str
    Email: EmailStr
    username: str
    id: int
    class Config:
        orm_mode = True 

class UpdateUser(CreateUser):
    pass
################################################################################
##############################  Registration   #################################

class AllUser(CreateUser):
    pass




class LoginUser(BaseModel):
    username: EmailStr
    password: str

class SpecificUser(BaseModel):
    fname: str
    lname: str
    username: str

#######################################################################################
##############################  Transaction History   #################################
    

class TranxGLDb(BaseModel):    
    amount: int
    currency: str
    payout: int
    Success: bool = False
    user: CreateUserRes

    class Config:
        orm_mode = True 


###########################################################################
############################  Token #######################################
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Votes(BaseModel):
    tranx_id: int
    dir: conint(le=1)
