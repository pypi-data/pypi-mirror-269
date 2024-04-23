import asyncio
import json
import sys

sys.path.append("/root/lingxiao/st-sdk/")
sys.path.append("/root/lingxiao/st-sdk/stsdk")

from stsdk.utils.websocket import Websocket

DMS_BASE_HTTP_URL = "ws://47.91.25.224:5002"

ws = Websocket(DMS_BASE_HTTP_URL + "/ws/dms")
req = {
    "event": "sub",
    "topic": "bbo.EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
}
ws.register(json.dumps(req))
asyncio.run(ws.run())
