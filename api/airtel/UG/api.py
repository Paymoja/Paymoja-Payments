import json
from schemas.payments_schema import IncomingPaymentSchema, IncomingDisbursementSchema
from .base import AirtelUGBase


class AirtelUGPayments(AirtelUGBase):

    def __init__(self, settings):
        self.client_id = settings['client_id']
        self.client_secret = settings['client_secret']
        self.url = settings['base_url']
        self.pin = settings['pin']

    async def get_bearer_token(self):
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }

        request_data = json.dumps(data)

        response = await self.api_request('post', '/auth/oauth2/token', request_data)
        return response

    async def ussd_push_transaction(self, request_data: IncomingPaymentSchema):
        """This API is used to request a payment from a consumer(Payer). The consumer(payer) will be asked to
        authorize the payment. After authorization, the transaction will be executed. """

        response = await self.api_request('post', '/merchant/v1/payments/', json.dumps(request_data))
        return response

    async def payments_refund_transaction(self, airtel_money_id: str):
        """This API is used to make full refunds to Partners."""
        data = {
            "transaction": {
                "airtel_money_id": airtel_money_id
            }
        }

        request_data = json.dumps(data)

        response = await self.api_request('post', '/standard/v1/payments/refund', request_data)
        return response

    async def payment_transaction_inquiry(self, transaction_id):
        """This API gets the transaction status corresponding to the requested External Id."""
        response = await self.api_request('get', '/standard/v1/payments/{}'.format(transaction_id))
        return response

    async def disbursement_transaction(self, disbursement_schema: IncomingDisbursementSchema):
        """This API is used to transfer an amount from the own account to a payee account."""
        response = []
        for disbursement in disbursement_schema.disbursement_details:
            data = {
                "payee": {
                    "msisdn": disbursement.msisdn
                },
                "reference": disbursement.reference,
                "pin": self.pin,
                "transaction": {
                    "amount": disbursement.amount,
                    "id": disbursement.payment_instance_id
                }
            }

            request_data = json.dumps(data)

            api_response = await self.api_request('post', '/standard/v1/disbursements/', request_data)
            response.append(api_response)
        return response

    async def disbursement_transaction_inquiry(self, transaction_id):
        """This API gets the transaction status corresponding to the requested External Id."""
        response = await self.api_request('get', '/standard/v1/disbursements/{}'.format(transaction_id))
        return response
