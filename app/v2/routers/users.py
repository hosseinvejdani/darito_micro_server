from fastapi import Body,APIRouter
from pydantic import BaseModel
from app.v2.models.models import ChangePhoneNumber, PhoneNumber, Unknown_SMS
from pymongo import MongoClient
import datetime


# ==============================================================
# ==============================================================
client = MongoClient("mongodb://localhost:27017")
database = client["darito"]
users_collection = database["user"]



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


# ==============================================================
router = APIRouter()


@router.get("/users/get_total_users/")
def get_total_users():
    count = users_collection.count_documents({})
    return {"total_userss": count}


@router.post("/users/add_user_or_update_login_info/")
def add_user_or_update_login_info(phone_number:PhoneNumber):
    number = phone_number.number
    #---------------
    response = addNewUserIfNotExistOrUpdateLoginInfo(number=number)
    return {"response":response}

@router.post("/users/change_user_number/")
def change_user_number(numbers:ChangePhoneNumber):
    old_number = numbers.old_number
    new_number = numbers.new_number
    #---------------
    response = changePhoneNumber(old_number,new_number)

    return {"response":response}







