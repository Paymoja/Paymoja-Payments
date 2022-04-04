from .api import AirtelUGPayments
from ...information_handler import InformationHandler


class PaymentInformationHandler(InformationHandler):

    def __init__(self, settings):
        self.client = AirtelUGPayments(settings)

    async def get_bearer_token(self):
        return await self.client.get_bearer_token()

