import datetime
import random
from fastapi import APIRouter, Body
import requests 
from app import constants
from app.v2.models.models import PhoneNumber, Unknown_SMS
from pymongo import MongoClient



def generate_random_code():
   list = [str(random.randint(1,9))]
   for i in range(4):
      list.append(str(random.randint(0,9)))
   return ''.join(list)

# sms.ir configuration
sms_url = constants.sms_url
sms_headers = {"Content-Type": "application/json","X-API-KEY": constants.X_API_KEY}

# ==============================================================
client = MongoClient("mongodb://localhost:27017")
database = client["darito"]
unkhnown_sms_collection = database["unkhnown_sms"]

# ==============================================================
router = APIRouter()

@router.post("/sms/send_verification_sms/")
def send_verification_sms(phone_number:PhoneNumber = Body(default=None)):

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

@router.post("/sms/add_unkhnown_sms/")
def add_unkhnown_sms(unknown_sms:Unknown_SMS):
    dateTime = datetime.datetime.utcnow()
    result = unkhnown_sms_collection.insert_one({"userNumber":unknown_sms.userNumber,"problem":unknown_sms.problem,"body":unknown_sms.body,"onSave":dateTime})
    return {"response":"unkhnown_sms added successfully to the database"}