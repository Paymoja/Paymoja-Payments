from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Request
from api.payment_handler import BasePaymentHandler
from dependencies.db import get_db

router = APIRouter(
    prefix='/api/ug/airtel',
    tags=['Airtel Uganda Payments'],
    responses={404: {"description": "oops can't help you with that!"}},
)


@router.post("/callback")
async def callback_url(background_tasks: BackgroundTasks, request: Request, db=Depends(get_db)):
    try:

        request = await request.json()

        print(request)

        def save_call_back():
            base_payment = BasePaymentHandler()
            return base_payment.save_incoming_callback(db, request, "airtel")

        background_tasks.add_task(save_call_back)

        message = "callback: {} received".format(request)
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return {"status_code": "200", "message": message}


@router.post("/callback/test")
async def callback_url_uat(background_tasks: BackgroundTasks, request: Request, db=Depends(get_db)):
    try:

        request = await request.json()

        def save_call_back():
            base_payment = BasePaymentHandler()
            return base_payment.save_incoming_callback(db, request, "airtel")

        background_tasks.add_task(save_call_back)

        message = "callback: {} received".format(request)
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return {"status_code": "200", "message": message}
