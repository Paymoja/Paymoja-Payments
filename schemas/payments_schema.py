from pydantic import BaseModel
from typing import Optional, List
from models.payments_model import CountryCodesEnum, PaymentStatusEnum, CurrencyCodesEnum


class IncomingPaymentSchema(BaseModel):
    payment_instance_id: str
    currency: CurrencyCodesEnum
    originator: str
    country: CountryCodesEnum
    msisdn: str
    amount: str
    provider: str
    reference: str
    status: PaymentStatusEnum


class DisbursementSchema(BaseModel):
    payment_instance_id: Optional[str]
    currency: CurrencyCodesEnum
    originator: str
    country: CountryCodesEnum
    msisdn: str
    amount: str
    provider: str
    reference: str
    status: PaymentStatusEnum


class IncomingDisbursementSchema(BaseModel):
    disbursement_details: List[DisbursementSchema]
