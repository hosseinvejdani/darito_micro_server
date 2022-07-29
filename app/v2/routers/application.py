from fastapi import APIRouter


router = APIRouter()


@router.get("/application/get_update_message/")
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

@router.get("/application/get_latest_version/")
def get_latest_version():
    return {"latest_version": "1.6.2"}