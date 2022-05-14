import json
import structlog
from fastapi import HTTPException
import requests
from schemas.payments_schema import IncomingPaymentSchema, IncomingDisbursementSchema
from .base import AirtelUGBase

struct_logger = structlog.get_logger(__name__)


class AirtelUGPayments(AirtelUGBase):

    def __init__(self, settings):
        self.client_id = settings['client_id']
        self.client_secret = settings['client_secret']
        self.url = settings['base_url']
        self.pin = settings['pin']
        self.bearer_token = self.get_bearer_token()

    def get_bearer_token(self):
        try:
            headers = {
                'Content-Type': 'application/json'
            }

            request_data = json.dumps({
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials"
            })

            response = self.api_request('post', 'auth/oauth2/token', headers, request_data)

            return json.loads(response)['access_token']

        except Exception as ex:
            raise HTTPException(status_code=404, detail="unable to send get bearer token {}".format(ex))

    def ussd_push_transaction(self, payment_schema: IncomingPaymentSchema):
        """This API is used to request a payment from a consumer(Payer). The consumer(payer) will be asked to
        authorize the payment. After authorization, the transaction will be executed. """

        try:

            url = 'https://openapi.airtel.africa/merchant/v1/payments/'

            headers = {
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'X-Country': 'UG',
                'X-Currency': 'UGX',
                'Authorization': 'Bearer {}'.format(self.bearer_token)
            }

            payload = {
                "reference": payment_schema.reference,
                "subscriber": {
                    "country": "UG",
                    "currency": "UGX",
                    "msisdn": 706748530  # payment_schema.msisdn
                },
                "transaction": {
                    "amount": payment_schema.amount,
                    "country": "UG",
                    "currency": "UGX",
                    "id": payment_schema.payment_instance_id
                }
            }

            response = requests.request("POST", url, headers=headers, json=payload)

            print(response.text)
            return json.loads(response.text)

        except Exception as ex:

            return ex

    def disbursement_transaction(self, disbursement_schema: IncomingPaymentSchema):
        """This API is used to transfer an amount from the own account to a payee account."""
        response = []

        url = "https://openapi.airtel.africa/standard/v1/disbursements/"

        print(self.bearer_token)

        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'X-Country': 'UG',
            'X-Currency': 'UGX',
            'Authorization': 'Bearer {}'.format(self.bearer_token)
        }

        payload = {
            "payee": {
                "msisdn": 700707701
            },
            "reference": disbursement_schema.reference,
            "pin": self.pin_encryption("0486"),
            "transaction": {
                "amount": 1000,
                "id": disbursement_schema.payment_instance_id
            }
        }

        response = requests.request("POST", url, headers=headers, json=payload)

        print(response.text)
        return json.loads(response.text)

        # for disbursement in disbursement_schema.disbursement_details:
        #     data = {
        #         "payee": {
        #             "msisdn": disbursement.msisdn
        #         },
        #         "reference": disbursement.reference,
        #         "pin": self.pin,
        #         "transaction": {
        #             "amount": disbursement.amount,
        #             "id": disbursement.payment_instance_id
        #         }
        #     }
        #
        #     request_data = json.dumps(data)
        #
        #     api_response = await self.api_request('post', '/standard/v1/disbursements/', request_data)
        #     response.append(api_response)
        # return response

    async def disbursement_transaction_inquiry(self, transaction_id):
        """This API gets the transaction status corresponding to the requested External Id."""
        response = await self.api_request('get', '/standard/v1/disbursements/{}'.format(transaction_id))
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
