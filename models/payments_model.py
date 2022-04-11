from sqlalchemy.orm import relationship

from sqlalchemy import Column, ForeignKey, String, JSON, DateTime, func, BigInteger
from sqlalchemy import Enum as SaEnum

from utils.database import Base
from enum import Enum


class PaymentStatusEnum(str, Enum):
    RECEIVED = 'RECEIVED'  # init state; received but not yet processed
    SENDING = 'SENDING'  # converted to integration and in process of being sent
    SENT = 'SENT'  # end state
    ERROR = 'ERROR'  # Could not be sent


class CountryCodesEnum(str, Enum):
    UG = 'UG'


class CurrencyCodesEnum(str, Enum):
    UGX = 'UGX'


class IncomingPayment(Base):
    __tablename__ = "incoming_payment"

    id = Column(BigInteger, primary_key=True, index=True)
    originator = Column(String(255), index=True, nullable=True)
    provider = Column(String(255), index=True, nullable=True)
    instance_payment_id = Column(String(255), index=True, unique=True, nullable=True)
    client_id = Column(String(255), index=True)
    reference = Column(String(255), index=True, nullable=True)
    provider_reference_id = Column(String(255), index=True, nullable=True)
    response_data = Column(JSON, nullable=True)
    request_data = Column(JSON, nullable=True)
    country_code = Column(String(255))
    upload_code = Column(String(255), index=True, nullable=True)
    upload_desc = Column(String(255), nullable=True)
    issue_date = Column(DateTime(timezone=True))
    date_last_modified = Column(DateTime(timezone=True))
    status = Column(SaEnum(PaymentStatusEnum))

    _request_payment = None

    class Config:
        orm_mode = True

    @property
    def request_payment(self):
        return self._request_payment


class OutgoingPayment(Base):
    __tablename__ = "outgoing_payments"

    id = Column(BigInteger, primary_key=True, index=True)
    originator = Column(String(255), index=True, nullable=True)
    provider = Column(String(255), index=True, nullable=True)
    instance_payment_id = Column(String(255), index=True, unique=True, nullable=True)
    client_id = Column(String(255), index=True)
    reference = Column(String(255), index=True, nullable=True)
    provider_reference_id = Column(String(255), index=True, nullable=True)
    response_data = Column(JSON, nullable=True)
    request_data = Column(JSON, nullable=True)
    country_code = Column(String(255))
    upload_code = Column(String(255), index=True, nullable=True)
    upload_desc = Column(String(255), nullable=True)
    issue_date = Column(DateTime(timezone=True))
    date_last_modified = Column(DateTime(timezone=True))
    status = Column(SaEnum(PaymentStatusEnum))

    _request_payment = None

    class Config:
        orm_mode = True

    @property
    def request_payment(self):
        return self._request_payment


class CallBack(Base):
    __tablename__ = "call_back"

    id = Column(BigInteger, primary_key=True, index=True)
    provider = Column(String(255), index=True, nullable=True)
    callback_data = Column(JSON, nullable=True)
    issue_date = Column(DateTime(timezone=True))
    date_last_modified = Column(DateTime(timezone=True))

    class Config:
        orm_mode = True