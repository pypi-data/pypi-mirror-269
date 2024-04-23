import json

from stsdk.common.key import (
    DMS_BBO,
    DMS_KLINE,
    DMS_LOB,
    DMS_TRADE,
)
from stsdk.utils.config import config
from stsdk.utils.websocket import Websocket


class DMSWS:
    def __init__(self):
        self.DMS_BASE_WS_URL = config.DMS_BASE_WS_URL
        self.ws = Websocket(self.DMS_BASE_WS_URL + "/ws/dms")

    def run(self, consumer):
        self.ws.run(consumer)

    def bbo(self, instrument_id):
        req = {
            "event": "sub",
            "topic": f"{DMS_BBO}.{instrument_id}",
        }
        self.ws.registerEvent(json.dumps(req))

    def lob(self, instrument_id):
        req = {
            "event": "sub",
            "topic": f"{DMS_LOB}.{instrument_id}",
        }
        self.ws.registerEvent(json.dumps(req))

    def kline(self, instrument_id):
        req = {
            "event": "sub",
            "topic": f"{DMS_KLINE}.{instrument_id}",
        }
        self.ws.registerEvent(json.dumps(req))

    def trade(self, instrument_id):
        req = {
            "event": "sub",
            "topic": f"{DMS_TRADE}.{instrument_id}",
        }
        self.ws.registerEvent(json.dumps(req))
