from ast import Not
from urllib import response
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

class ChangePhoneNumber(BaseModel):
    old_number: str
    new_number: str

def generate_random_code():
   list = [str(random.randint(1,9))]
   for i in range(4):
      list.append(str(random.randint(0,9)))
   return ''.join(list)


def addNewUserIfNotExistOrUpdateLoginInfo(number:str):
    result = users.find_one({"number":number})
    dateTime = datetime.datetime.utcnow()
    if result == None:
        response = users.insert_one({"number":number,"lastLogin":dateTime})
        return {"response":response}
    else:
        newvalue = {"$set":{"lastLogin": dateTime}}
        response = users.update_one({"number":number},newvalue)
        return {"response":response}


def changePhoneNumber(old_number:str,new_number:str):
    newvalue = {"$set":{"number": new_number}}
    response = users.update_one({"number":old_number},newvalue)
    #
    # TODO : you should also apply change for all other recodrs in future
    return {"response":response}




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
    
    response = requests.post(sms_url, headers=sms_headers, json=data)
    # ------------------------------------
    if response.status_code == 200:
        return {"token":token}
    #
    return {"token": None,"error":"there was an error while sending message! please try again..."}


@app.post("/add_user_or_update_login_info")
def add_user_or_update_login_info(phone_number:PhoneNumber):
    number = phone_number.number
    #---------------
    response = addNewUserIfNotExistOrUpdateLoginInfo(number=number)
    return {"response":response}

@app.post("/change_user_number")
def change_user_number(numbers:ChangePhoneNumber):
    old_number = numbers.old_number
    new_number = numbers.new_number
    #---------------
    response = changePhoneNumber(old_number,new_number)
    return {"response":response}




