from typing import List
from fastapi import Body,APIRouter
from pymongo import MongoClient
from app.v2.models.models import User


# ==============================================================
# ==============================================================
client = MongoClient("mongodb://localhost:27017")
database = client["darito"]
users_collection = database["user"]


# ==============================================================
router = APIRouter()

# a function get all users
@router.get("/users", response_model=List[User],tags=["users"],description="Get all users")
async def get_users():
    users = users_collection.find()
    return list(users)

# a method for count all Users from Database
@router.get("/users/count",tags=["users"],description="Count all users in database")
def countAllUsers():
    count = users_collection.count_documents({})
    return {"total_users": count}

# a method for getting user by userName
@router.get("/user/{userName}",tags=["users"],description="Get user by userName")
async def getUserByUserName(userName:str):
    result = users_collection.find_one({"userName":userName},{'_id': 0})
    if result == None:
        return {"result":f"user {userName} not found"}
    return {"user":result}

# a method for checking userName availability
@router.get("/user/availability/{userName}",tags=["users"],description="Check userName availability")
async def checkUserNameAvailability(userName:str):
    result = users_collection.find_one({"userName":userName},{'_id': 0})
    if result == None:
        return {"message":f"user {userName} is available","available":True}
    else:
        return {"message":f"user {userName} is not available","available":False}

# a method for createUser
@router.post("/users/create",tags=["users"],description="Create user")
async def createUser(user: User):
    result = users_collection.find_one({"userName":user.userName},{'_id': 0})
    if result == None:
        response = users_collection.insert_one(user.dict())
        return {"result":"user was added to the database successfully."}
    else:
        return {"result":"user was exists on the database."}



# a mehtod updating User in Database
@router.put("/users/update/{userName}",tags=["users"],description="Update user in database")
async def updateUser(userName:str,user: User):
    result = users_collection.find_one({"userName":userName},{'_id': 0})
    if result == None:
        return {"result":f"user {userName} not found"}
    else:
        newvalue = {"$set":user.dict()}
        response = users_collection.update_one({"userName":userName},newvalue)
        return {"message":f"user {userName} was updated successfully.","new_user":newvalue}



# a method for delete User From Database
@router.delete("/users/delete/{userName}",tags=["users"],description="Delete user from database")
async def deleteUser(userName:str):    
    result = users_collection.find_one({"userName":userName},{'_id': 0})
    if result == None:
        return {"result":f"user {userName} not found"}
    else:
        response = users_collection.delete_one({"userName":userName})
        return {"result":f"user {userName} was deleted from database successfully."} 










