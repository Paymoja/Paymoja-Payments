import importlib

from api.payment_handler import BasePaymentHandler
from models.payments_model import IncomingPayment
from schemas.common_schema import AuthInterfaceSchema
from dependencies.settings import ClientInterfaceSettings
from schemas.payments_schema import IncomingPaymentSchema


class PaymentService:

    def __init__(self, interface_details: AuthInterfaceSchema):
        self.country_code = interface_details.country_code
        self.client_id = interface_details.client_id
        self.provider = interface_details.provider
        self.client = ClientInterfaceSettings.configure_settings()[self.country_code][self.provider][self.client_id]
        self.settings = self.client['staging'] if self.client['testing'] else self.client['production']

        self.originator = self.settings['originator']

        self.information_module = importlib.import_module(
            "api.%s.%s.information_handler" % (self.provider, self.country_code))
        self.information_handler = getattr(self.information_module, "PaymentInformationHandler")
        self.information_manager = self.information_handler(self.settings)

        self.payment_module = importlib.import_module(
            "api.%s.%s.payment_handler" % (self.provider, self.country_code))
        self.payment_handler = getattr(self.payment_module, "PaymentHandler")
        self.payment_manager = self.payment_handler(self.settings)

    async def incoming_information_request(self, information_request: str):
        return await self.information_manager.get_information_request(
            information_request
        )

    async def create_outgoing_payment(self, db, incoming_payment: IncomingPaymentSchema):
        new_payment = self.payment_manager.create_outgoing_payment(db,
                                                                   incoming_payment,
                                                                   self.originator,
                                                                   self.country_code,
                                                                   self.provider,
                                                                   self.client_id)
        return new_payment

    async def send_payment(self, db, payment: IncomingPayment):
        payment = await self.payment_manager.send_payment(db, payment)
        return payment

    async def send_disbursement(self, db, payment: IncomingPayment):
        disbursement = await self.payment_manager.send_disbursement(db, payment)
        return disbursement

    async def incoming_call_back(self,db, data,provider):
        base_payment = BasePaymentHandler()
        return base_payment.save_incoming_callback(db, data,provider)

