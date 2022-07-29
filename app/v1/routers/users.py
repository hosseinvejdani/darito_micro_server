from fastapi import APIRouter
from fastapi import Body
from pydantic import BaseModel
import random
import requests
from app import constants
from pymongo import MongoClient
import datetime

# sms.ir configuration
sms_url = constants.sms_url
sms_headers = {"Content-Type": "application/json","X-API-KEY": constants.X_API_KEY}

# ==============================================================
# ==============================================================
client = MongoClient("mongodb://localhost:27017")
database = client["darito"]
unkhnown_sms_collection = database["unkhnown_sms"]
users_collection = database["user"]



class Unknown_SMS(BaseModel):
    userNumber:str
    problem:str 
    body:str 

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
    result = users_collection.find_one({"number":number})
    dateTime = datetime.datetime.utcnow()
    if result == None:
        response = users_collection.insert_one({"number":number,"lastLogin":dateTime})
        return {"result":"added new user to the database successfully."}
    else:
        newvalue = {"$set":{"lastLogin": dateTime}}
        response = users_collection.update_one({"number":number},newvalue)
        return {"result":"user number was exists on the database.so the user lastLogin info updated successfully."}


def changePhoneNumber(old_number:str,new_number:str):
    newvalue = {"$set":{"number": new_number}}
    response = users_collection.update_one({"number":old_number},newvalue)
    #
    return {"result":f"The number {old_number} was deleted from database and added {new_number} as new user phone number"}


router = APIRouter()


@router.get("/get_update_message/")
def get_update_message():
    # target_version = ["1.2.0","1.4.0","1.5.0","1.6.1"] # or "any"
    target_version = [] # or "any"
    repeat = True
    title = "به روز رسانی مهم"
    message = "کاربر گرامی، با توجه به ارتقاء سرور های داریتو در جهت بهبود کیفیت خدمات به شما عزیزان، به روز رسانی جدید در کافه بازار منشتر شد. لذا جهت حفظ اطلاعات ثبت شده در اپلیکیشن لازم است نسخه جدید را نصب نمایید."
    hard_update = True
    #
    data = {"target_version": target_version,"repeat":repeat, "title":title,"message":message,"hard_update":hard_update}
    return data

@router.get("/get_latest_version/")
def get_latest_version():
    return {"latest_version": "1.6.2"}

@router.get("/get_total_users/")
def get_total_users():
    count = users_collection.count_documents({})
    return {"total_userss": count}


@router.post("/send_verification_sms/")
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


@router.post("/add_user_or_update_login_info/")
def add_user_or_update_login_info(phone_number:PhoneNumber):
    number = phone_number.number
    #---------------
    response = addNewUserIfNotExistOrUpdateLoginInfo(number=number)
    return {"response":response}

@router.post("/change_user_number/")
def change_user_number(numbers:ChangePhoneNumber):
    old_number = numbers.old_number
    new_number = numbers.new_number
    #---------------
    response = changePhoneNumber(old_number,new_number)

    return {"response":response}



@router.post("/add_unkhnown_sms/")
def add_unkhnown_sms(unknown_sms:Unknown_SMS):
    dateTime = datetime.datetime.utcnow()
    result = unkhnown_sms_collection.insert_one({"userNumber":unknown_sms.userNumber,"problem":unknown_sms.problem,"body":unknown_sms.boy,"onSave":dateTime})
    return {"response":"unkhnown_sms added successfully to the database"}



