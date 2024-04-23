from stsdk.api.ws.dms import DMSWS
from stsdk.common.key import DMS_BBO

ws = DMSWS()


class ST:
    def init_params(self):
        self.register(
            DMS_BBO,
            self.handle_bbo,
            instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        )

    def handle_bbo(self, message):
        print("message", message)


st = ST()
