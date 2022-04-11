import asyncio
import json
import time

import httpx
import structlog
from requests import HTTPError

import requests

start_time = time.time()

struct_logger = structlog.get_logger(__name__)


class HttpxRequest:
    def __init__(self, url, timeout=20):
        self.url = url
        self.timeout = httpx.Timeout(timeout)
        self.client = httpx.AsyncClient(verify=False)

    async def httpx_request(self, method, data, headers=None):
        try:
            response = "Unable to send httpx request, wrong parameters"
            if method.upper() == "POST":
                struct_logger.info(event="http request", json=data, headers=headers, url=self.url, method=method)
                response = await self.client.post(self.url,
                                                  json=data,
                                                  timeout=self.timeout,
                                                  headers=headers

                                                  )
            elif method.upper() == "GET":
                response = await self.client.get(self.url,
                                                 timeout=self.timeout,
                                                 headers=headers
                                                 )

            elif method.upper() == "PUT":
                response = await self.client.put(self.url,
                                                 timeout=self.timeout,
                                                 headers=headers
                                                 )

            await self.client.aclose()

            return response
        except Exception as ex:
            struct_logger.info(event='HttpxRequest', error=str(ex), request=data)
            return {"error": str(ex), "status": "", "request": data}

    def http_request(self, method, data, headers=None):
        try:
            response = "Unable to send http request, wrong parameters"
            if method.upper() == "POST":
                struct_logger.info(event="http request", json=data, headers=headers, url=self.url, method=method)
                response = requests.request(method,
                                            self.url,
                                            data=data,
                                            headers=headers

                                            )
            elif method.upper() == "GET":
                response = requests.request(method,
                                            self.url,
                                            headers=headers
                                            )

            elif method.upper() == "PUT":
                response = requests.request(method,
                                            self.url,
                                            headers=headers
                                            )

            return response
        except Exception as ex:
            struct_logger.info(event='HttpRequest', error=str(ex), request=data)
            return {"error": str(ex), "status": "", "request": data}
