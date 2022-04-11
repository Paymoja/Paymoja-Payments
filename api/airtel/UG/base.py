import json

import structlog

from dependencies.http_requests import HttpxRequest

struct_logger = structlog.get_logger(__name__)


class AirtelUGBase:

    def __init__(self, settings):
        self.url = settings['base_url']

    def api_request(self, method, path, headers, data):
        req = HttpxRequest(self.url + path)

        api_response = req.http_request(method, data, headers=headers)

        struct_logger.info(event='airtel_ug_api_request',
                           message="sending airtel uganda api request",
                           interface=self.url + path,
                           data=data,
                           method=method,
                           api_response=api_response
                           )

        return api_response.text

    def pin_encryption(self, msg):
        from Crypto.PublicKey import RSA
        from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
        from base64 import b64decode, b64encode
        pubkey = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCkq3XbDI1s8Lu7SpUBP+bqOs/MC6PKWz6n/0UkqTiOZqKqaoZClI3BUDTrSIJsrN1Qx7ivBzsaAYfsB0CygSSWay4iyUcnMVEDrNVOJwtWvHxpyWJC5RfKBrweW9b8klFa/CfKRtkK730apy0Kxjg+7fF0tB4O3Ic9Gxuv4pFkbQIDAQAB"
        # msg = "test"
        keyDER = b64decode(pubkey)
        keyPub = RSA.importKey(keyDER)
        cipher = Cipher_PKCS1_v1_5.new(keyPub)
        cipher_text = cipher.encrypt(msg.encode())
        emsg = b64encode(cipher_text)
        return emsg
