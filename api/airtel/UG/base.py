import structlog

from dependencies.http_requests import HttpxRequest

struct_logger = structlog.get_logger(__name__)


class AirtelUGBase:

    def __init__(self, settings):
        self.url = settings['base_url']

    async def api_request(self, method, path, data={}):
        headers = {
            'content-type': 'application/json',
            'accept': '*/*',
        }

        req = HttpxRequest(self.url + path)

        api_response = await req.httpx_request(method, data, headers=headers)

        struct_logger.info(event='airtel_ug_api_request',
                           message="sending airtel uganda api request",
                           interface=self.url + path,
                           data=data,
                           method=method,
                           api_response=api_response
                           )

        return api_response.json()
