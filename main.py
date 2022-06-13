from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional
import random
import requests
from pymongo import MongoClient
import datetime


# sms.ir configuration
sms_url = "https://api.sms.ir/v1/send/verify"
sms_headers = {"Content-Type": "application/json","X-API-KEY": "dFPwXdS4B5TTLqQuZ5QCNyoBzwa1GtkCqhMVb25nf5NUFEYlAM3Aa38mNS0iKnfv"}



class PhoneNumber(BaseModel):
    number:str 
    token:Optional[str] = None

def generate_random_code():
   list = [str(random.randint(1,9))]
   for i in range(4):
      list.append(str(random.randint(0,9)))
   return ''.join(list)

# def saveToDB(number: str, token: str):
#     createdAt = datetime.datetime.utcnow()
#     result = tokens.insert_one({"number":number,"token":token,"createdAt":createdAt})
#     return result


# def addNewUserIfNotExist(number:str):
#     result = users.find_one({"number":number})
#     dateTime = datetime.datetime.utcnow()
#     if result == None:
#         users.insert_one({"number":number,"lastLogin":dateTime})
#     else:
#         newvalue = {"$set":{"lastLogin": dateTime}}
#         users.update_one({"number":number},newvalue)


# def check_token_validation(number:str,token:str):
#     result = tokens.find_one({"number":number,"token":token})
#     if result == None:
#         return False

#     addNewUserIfNotExist(number)
#     return True


# ==============================================================
# ==============================================================
client = MongoClient("mongodb://localhost:27017")
database = client["darito"]
tokens = database["token"]
users = database["user"]
#
app = FastAPI()

@app.get("/get_latest_version")
def get_latest_version():
    return {"latest_version": "1.0.0"}


@app.post("/send_verification_sms")
def send_verification_sms(phone_number:PhoneNumber):

    number = phone_number.number
    token = generate_random_code()

    # # ------------------------------------
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
    
    response = requests.post(sms_url, headers=sms_headers, json=data)
    # ------------------------------------
    if response.status_code == 200:
        # saveToDB(number = number, token = token)
        return {"token":token}
    #
    return {"token":"---","error":"there was an error while sending message! please try again..."}


# TODO : remove this 
# @app.post("/verify_otp_token")
# def verify_otp_token(phone_number:PhoneNumber):
#     number = phone_number.number
#     token = phone_number.token
#     #---------------
#     is_valid_token = check_token_validation(number, token)
#     return {"isValid":is_valid_token}


# TODO : add new method for adding new user to database 

# TODO : add new method for updating user in database

# TODO : add new method for changing number for user in all docs in database 