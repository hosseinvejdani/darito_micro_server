from fastapi import  FastAPI

from .v1.routers import  users as users_v1
from .v2.routers import  users as users_v2
from .v2.routers import  sms as sms_v2
from .v2.routers import  application as application_v2

app = FastAPI()

app.include_router(users_v1.router)

# # ---------------------------------
v2 = FastAPI()
v2.include_router(users_v2.router)
v2.include_router(sms_v2.router)
v2.include_router(application_v2.router)

# ---------
app.mount("/api/v2", v2)