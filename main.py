# from typing import Union
from fastapi import FastAPI, Body
# from pydantic import BaseModel
# from typing import Optional
# from deta import Deta
# import random
# import requests


# sms.ir configuration
# sms_url = "https://api.sms.ir/v1/send/verify"
# sms_headers = {"Content-Type": "application/json","X-API-KEY": "dFPwXdS4B5TTLqQuZ5QCNyoBzwa1GtkCqhMVb25nf5NUFEYlAM3Aa38mNS0iKnfv"}

# deta base configuration
# A Project Key must to be provided in the request headers as a value for the X-API-Key key for authentication.
# deta_base_url = "https://database.deta.sh/v1/c0air9ks/OTPcode/"
# deta_base_headers = {"Content-Type": "application/json","X-API-KEY": "c0air9ks_6TYEjPaW7ALs1rYb6kguBqgFPb6qmmDf"}

# class PhoneNumber(BaseModel):
#     number:str 
#     token:Optional[str] = None

# def generate_random_code():
#    list = [str(random.randint(1,9))]
#    for i in range(4):
#       list.append(str(random.randint(0,9)))
#    return ''.join(list)

# def saveToDB(data:dict):
#     response = requests.post(deta_base_url+"/items", headers=deta_base_headers, json={"item":data})
#     print(response)
#     # This how to connect to or create a database.
#     # otp = deta.Base("OTPcode")
#     # otp.put(data,expire_in=60)

# def check_token_validation(number:str,token:str):
#     otp = deta.Base("OTPcodes")
#     token_in_db = otp.get(number)
#     return token==token_in_db


# ==============================================================
# ==============================================================
# ==============================================================

# Initialize with a Project Key
# deta = Deta("c0air9ks_6TYEjPaW7ALs1rYb6kguBqgFPb6qmmDf",project_id="c0air9ks")
#
app = FastAPI()

@app.get("/get_latest_version")
def get_latest_version():
    return {"latest_version": "1.0.0"}


# @app.post("/send_verification_sms")
# def send_verification_sms(phone_number:PhoneNumber):

#     number = phone_number.number
#     token = generate_random_code()

#     # # ------------------------------------
#     data =   {
#         "mobile": number[3:],
#         "templateId": 782582,
#         "parameters": [
#             {
#                 "name": "Code",
#                 "value": token
#             }
#         ]
#     }
    
#     response = requests.post(sms_url, headers=sms_headers, json=data)
#     # ------------------------------------
#     if response.status_code == 200:
#         saveToDB({number:token})
#     #
#     return response


# @app.post("/verify_otp_token")
# def verify_otp_token(phone_number:PhoneNumber):
#     number = phone_number.number
#     token = phone_number.token
#     #---------------
#     is_valid_token = check_token_validation(number, token)
#     return {"isValid":is_valid_token}


