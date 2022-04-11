import json
import structlog
from api.airtel.UG.api import AirtelUGPayments
from api.payment_handler import BasePaymentHandler
from schemas.payments_schema import IncomingPaymentSchema

struct_logger = structlog.get_logger(__name__)


class PaymentHandler(BasePaymentHandler):

    def __init__(self, settings):

        self.request_data = {}
        self.response_data = {}
        self.upload_code = ''
        self.upload_desc = ''
        self.json_data = {}
        self.reason = ''
        self.reason_code = ''
        self.api_response = None
        self.client = AirtelUGPayments(settings)

    async def convert_request(self, payment_schema: IncomingPaymentSchema):

        return payment_schema

    def _send_payment(self, request_data):
        return self.client.ussd_push_transaction(request_data)

    def _send_disbursement(self, request_data):
        return self.client.disbursement_transaction(request_data)

    def convert_response(self, response):

        try:

            return True, response
        except Exception as ex:

            return False, "response"
