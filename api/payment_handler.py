import json

import pyqrcode
import structlog
from pydantic import parse_obj_as
from models.payments_model import PaymentStatusEnum, IncomingPayment
from schemas.payments_schema import IncomingPaymentSchema
from dal.payments_dal import save_payment, create_outgoing_payment, get_payment

struct_logger = structlog.get_logger(__name__)


class BasePaymentHandler:
    '''
    Base class for integrations with tax services
    that involve sending invoices
    '''

    def __init__(self, settings):
        """
        Usually, some settings will be needed to initialize a client
        """
        pass

    def create_outgoing_payment(self,
                                db,
                                new_payment: IncomingPaymentSchema,
                                originator,
                                country_code,
                                provider,
                                client_id):
        new_payment = create_outgoing_payment(db,
                                              new_payment,
                                              originator,
                                              country_code,
                                              provider,
                                              client_id)

        struct_logger.info(event='create_outgoing_payment',
                           message="saving new payment",
                           payment=new_payment,
                           status="success"
                           )
        return new_payment

    async def send_payment(self, db, payment: IncomingPayment):
        """
        Sends the payment to the RA, using
        1. converts request_data to format the RA expects
        2. saves the response
        3. updates the payment status
        """

        if payment.status == PaymentStatusEnum.RECEIVED:
            request_payment = payment.request_payment or parse_obj_as(IncomingPaymentSchema, json.loads(payment.request_data))
            request_data = await self.convert_request(request_payment)
            payment.request_data = request_data
            payment.status = PaymentStatusEnum.SENDING

        elif payment.status == PaymentStatusEnum.SENT:

            return payment

        else:
            request_data = payment.request_data

        result = await self._send_payment(request_data)
        success, response_data = self.convert_response(result)

        struct_logger.info(event='payment handler',
                           message="sending payment upload request",
                           request=response_data,
                           status=success,
                           response=response_data
                           )

        payment.status = PaymentStatusEnum.SENT if success else PaymentStatusEnum.ERROR

        payment.response_data = response_data
        save_payment(db, payment)

        return payment

    async def convert_request(self, request_invoice: IncomingPaymentSchema):
        '''
        Takes a TaxInvoiceOutgoing and converts it to
        the representation the client expects. 
        '''
        return request_invoice

    def convert_response(self, response):
        '''
        From the response, determine if the payment request was successful
        And, if necessarry, convert the response data to json to save in
        response_data
        '''
        return True, response

    async def get_invoice_status(self, instance_invoice_id):

        """Get payment status from database"""
        pass

    @staticmethod
    def get_payment_by_id(db,
                          instance_payment_id,
                          country_code,
                          provider,
                          client_id):

        """Get payment from database"""

        return get_payment(db, instance_payment_id, country_code, provider, client_id)

    async def _get_all_payments(self):

        """Get payment all invoices from database"""
        raise NotImplementedError

    async def _send_payment(self, request_data):
        '''
        Actually send the payment
        '''
        raise NotImplementedError
