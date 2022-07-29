
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