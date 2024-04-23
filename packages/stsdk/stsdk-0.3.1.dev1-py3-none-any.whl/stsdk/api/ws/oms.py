import json

from stsdk.common.key import OMS_ORDER_UPDATE
from stsdk.utils.config import config
from stsdk.utils.websocket import Websocket

class OMSWS:

    def __init__(self):
        self.OMS_BASE_WS_URL = config.OMS_BASE_WS_URL
        self.ws = Websocket(self.OMS_BASE_WS_URL + "/ws/oms")

    def run(self, consumer):
        self.ws.run(consumer)

    def oms_order(self, strategy_id, account_id):
        req = {
            "event": "sub",
            "topic": OMS_ORDER_UPDATE,
            "strategy_id": strategy_id,
            "account_id": account_id,
        }
        self.ws.registerEvent(json.dumps(req))
