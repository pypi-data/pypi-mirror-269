import asyncio
import time

from stsdk.common.env import ENV_TEST
from stsdk.model.strategy_module import StrategyModule
from stsdk.utils.config import config
from stsdk.utils.log import log


class ST(StrategyModule):
    name = "ST"

    def init_params(self):
        log.info(f"init_params {self.name}")
        config.set_env(ENV_TEST)

    def start_trading_session(self):
        pass

    def run_on_data_feed(self, *args):
        pass


st = ST("1", "aris_test")


def place_order_for_position(instrument_id, price, size, side):
    st.place_order_signal(instrument_id, price, size, side)
    time.sleep(1)
    res = st.get_position(instrument_id)
    log.info("get_position: %s" % res)
    open_orders = st.get_open_orders(instrument_id)
    log.info("get_open_orders: %s" % open_orders)
    for order_id, open_order in open_orders.items():
        order = st.get_order_by_id(instrument_id, order_id)
        log.info("get_order_by_id: %s" % order)


def cancel_order_for_position(instrument_id, price, size, side):
    st.place_order_signal(instrument_id, price, size, side)
    time.sleep(1)
    res = st.get_position(instrument_id)
    log.info("get_position: %s" % res)
    open_orders = st.get_open_orders(instrument_id)
    log.info("get_open_orders: %s" % open_orders)


# 验证下单和撤单的时候，持仓是否正确
def order_for_position():
    instrument_id = "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED"
    place_order_for_position(instrument_id, "2290", "0.1", "buy")
    # order_id = "1jtb38z29s8cxou19t96eck300w9a8rl"
    # cancel_order_for_position(instrument_id, order_id)


async def main():
    order_for_position()


if __name__ == "__main__":
    asyncio.run(main())
