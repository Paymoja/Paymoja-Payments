from fastapi import Header, HTTPException
from services.payment_service import PaymentService
from schemas.common_schema import AuthInterfaceSchema
from dependencies.settings import ClientInterfaceSettings


async def verify_auth_details(x_provider: str = Header(...), x_client_id: str = Header(...), x_country_code=Header(...),
                              x_api_token=Header(...)):
    if not ClientInterfaceSettings.configure_settings()[x_country_code][x_provider][x_client_id]:
        raise HTTPException(status_code=400, detail="Payment Details header is invalid")

    interface_details = AuthInterfaceSchema(
        **{"country_code": x_country_code, "provider": x_provider, "api_token": x_api_token, "client_id": x_client_id})

    payment_service = PaymentService(interface_details)

    return payment_service
