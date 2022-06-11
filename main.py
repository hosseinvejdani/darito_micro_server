# from typing import Union
from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional
from deta import Deta
import random
import requests


# sms.ir configuration
url = "https://api.sms.ir/v1/send/verify"
headers = {"X-API-KEY": "dFPwXdS4B5TTLqQuZ5QCNyoBzwa1GtkCqhMVb25nf5NUFEYlAM3Aa38mNS0iKnfv"}

class PhoneNumber(BaseModel):
    number:str 
    token:Optional[str] = None

def generate_random_code():
   list = [str(random.randint(1,9))]
   for i in range(4):
      list.append(str(random.randint(0,9)))
   return ''.join(list)

def saveToDB(data:dict):
    # This how to connect to or create a database.
    otp = deta.Base("OTPcodes")
    otp.put(data,expire_in=60)

def check_token_validation(number:str,token:str):
    otp = deta.Base("OTPcodes")
    token_in_db = otp.get(number)
    return token==token_in_db

# Initialize with a Project Key
deta = Deta()
#
app = FastAPI()

@app.get("/get_latest_version")
def get_latest_version():
    return {"latest_version": "1.0.0"}


@app.post("/send_verification_sms")
def send_verification_sms(phone_number:PhoneNumber):
    number = phone_number.number
    token = generate_random_code()
    # ------------------------------------
    data =   {
    "mobile": number[3:],
    "templateId": 782582,
    "parameters": [
      {
        "name": "Code",
        "value": token
      }
     ]
    }
    response = requests.post(url, headers=headers, json=data)
    # ------------------------------------
    if response.status_code == 200:
        saveToDB({number:token})


@app.post("/verify_otp_code")
def verify_otp_code(phone_number:PhoneNumber):
    number = phone_number.number
    token = phone_number.token
    #---------------
    is_valid_token = check_token_validation(number = number, token = token)
    return {"isValid":is_valid_token}


