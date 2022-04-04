from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, Header
from dependencies.auth_depencies import verify_auth_details
from dependencies.db import get_db
from schemas.payments_schema import IncomingPaymentSchema

router = APIRouter(
    prefix='/api',
    tags=['Pay-moja Payments'],
    responses={404: {"description": "oops can't help you with that!"}},
)


@router.get("/information/{information_request}")
async def incoming_information_request(information_request: str,
                                       information_service=Depends(verify_auth_details)
                                       ):
    try:
        message = await information_service.incoming_information_request(information_request)

    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return {"status_code": "200", "message": message}


@router.post("/payment/new")
async def incoming_invoice_request(incoming_payment: IncomingPaymentSchema,
                                   background_tasks: BackgroundTasks,
                                   payment_service=Depends(verify_auth_details),
                                   db=Depends(get_db)
                                   ):
    try:
        message = payment_service
        payment_saved = await payment_service.create_outgoing_payment(db, incoming_payment)

        async def send_new_payment():
            await payment_service.send_payment(db, payment_saved)

        background_tasks.add_task(send_new_payment)
        message = "Payment sent for processing"
    except Exception as ex:
        raise HTTPException(status_code=404, detail=str(ex))

    return {"status_code": "200", "message": message}
