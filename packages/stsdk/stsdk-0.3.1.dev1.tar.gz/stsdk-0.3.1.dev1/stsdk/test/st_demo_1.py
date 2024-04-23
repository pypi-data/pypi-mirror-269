import asyncio

from stsdk.common.env import ENV_TEST
from stsdk.common.key import (
    OMS_ORDER_UPDATE,
    ORDER_DIRECTION_BUY,
    POSITION_SIDE_LONG,
)
from stsdk.model.strategy_module import StrategyModule
from stsdk.utils.config import config
from stsdk.utils.log import log


class ST1(StrategyModule):
    name = "ST1"

    def __init__(self, strategy_id, account_id):
        config.set_env(ENV_TEST)
        super().__init__(strategy_id, account_id)

    def init_params(self):
        log.info("ST1 init_params")
        # self.register(
        #     DMS_BBO,
        #     self.handle_bbo,
        #     instrument_id="EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        # )
        # self.register(
        #     DMS_BBO,
        #     self.handle_btc_bbo,
        #     instrument_id="EXCHANGE_BINANCE.BTC-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        # )
        self.register(
            OMS_ORDER_UPDATE,
            self.handle_order_update,
            strategy_id=self.strategy_id,
            account_id=self.account_id,
        )

    def start_trading_session(self):
        pass

    def run_on_data_feed(self, *args):
        pass

    def handle_error(self, error):
        print("error", error)
        pass

    def handle_bbo(self, message):
        pass
        # log.info("bbo: ", message)

    def handle_btc_bbo(self, message):
        self.name = "btc update"
        # log.info("btc bbo", self.name)

    def handle_order_update(self, message):
        log.info(message)


async def main():
    st = ST1("1", "aris_test")
    st.register_instrument(
        "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        1000,
        1000,
    )
    st.place_order(
        "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        "2203",
        0.01,
        ORDER_DIRECTION_BUY,
        POSITION_SIDE_LONG,
    )


if __name__ == "__main__":
    asyncio.run(main())
