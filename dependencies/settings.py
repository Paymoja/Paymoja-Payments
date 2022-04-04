import json
from pathlib import Path

import structlog

struct_logger = structlog.get_logger(__name__)


class ClientInterfaceSettings:
    def __init__(self):
        pass

    @staticmethod
    def configure_settings():
        file = Path('settings.json').absolute()
        if not file.exists():
            struct_logger.error(event="configure_settings", error="settings file has not been found")
            raise Exception("settings file has not been file. Service can not continue, please see settings template")

        with open('settings.json') as fin:
            return json.load(fin)
