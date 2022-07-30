
from datetime import datetime
from pydantic import BaseModel

class Unknown_SMS(BaseModel):
    userNumber:str
    problem:str 
    body:str 

class PhoneNumber(BaseModel):
    number:str 

class ChangePhoneNumber(BaseModel):
    old_number: str
    new_number: str



# a User class with name,phone,email,birthdate,registerdated,lastlogin,isvip,isAuthorized,isActive,referalcode
class User(BaseModel):
    name: str = None
    phone: str = None
    email: str = None
    birthDate: datetime = None
    registerDate: datetime = None
    lastLogin: datetime = None
    referalCode: str = None
    isVip: bool = False
    isAuthorized: bool = False
    isActive: bool = False
