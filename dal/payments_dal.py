import structlog
from sqlalchemy.orm import Session

from models.payments_model import PaymentStatusEnum, IncomingPayment, OutgoingPayment
from schemas.payments_schema import IncomingPaymentSchema

struct_logger = structlog.get_logger(__name__)


def create_outgoing_payment(db: Session,
                            payment: IncomingPaymentSchema,
                            originator,
                            country_code,
                            provider,
                            client_id):
    """
    Saves a raw payment from upstream
    All the data gets jammed into 'request_data'
    status is RECEIVED
    The handler later takes this and converts it to integration specific representation
    (an outgoing payment)
    """

    try:

        payment_exists = get_payment(db, payment.payment_instance_id, country_code, provider, client_id)

        if not payment_exists:
            new_payment_details = {
                "request_data": payment.json(),
                "originator": originator,
                "provider": provider,
                "country_code": country_code,
                "reference": payment.reference,
                "status": PaymentStatusEnum.RECEIVED,
                "client_id": client_id,
                "instance_payment_id": payment.payment_instance_id
            }

            payment_base = IncomingPayment(**new_payment_details)
            new_payment = create_payment(db, payment_base)
            new_payment._request_payment = payment
            return new_payment

        return payment_exists

    except Exception as ex:

        struct_logger.error(event="create_outgoing_payment", error="Failed to save payment", message=str(ex))

        return None


def create_payment(db: Session, payment_details):
    new_payment = IncomingPayment(
        request_data=payment_details.request_data,
        originator=payment_details.originator,
        provider=payment_details.provider,
        instance_payment_id=payment_details.instance_payment_id,
        client_id=payment_details.client_id,
        reference=payment_details.reference,
        country_code=payment_details.country_code,
        upload_code=payment_details.upload_code,
        upload_desc=payment_details.upload_desc,
        status=payment_details.status
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment


def get_payment(db: Session, instance_payment_id: str, country_code: str, provider: str, client_id: str):
    payment = db.query(IncomingPayment).filter(
        IncomingPayment.instance_payment_id == instance_payment_id,
        IncomingPayment.country_code == country_code,
        IncomingPayment.provider == provider,
        IncomingPayment.client_id == client_id,
    ).one_or_none()

    if payment is None:
        return None

    return payment


def save_payment(db: Session, payment: IncomingPayment):
    db.add(payment)
    db.commit()


def get_payment_by_id(db: Session, instance_payment_id: str):
    return db.query(IncomingPayment).filter(
        IncomingPayment.instance_payment_id == instance_payment_id).first()


def get_disbursement_by_id(db: Session, instance_payment_id: str):
    return db.query(OutgoingPayment).filter(
        OutgoingPayment.instance_payment_id == instance_payment_id).first()
