import asyncio

from stsdk.common.key import DMS_BBO, OMS_ORDER_UPDATE
from stsdk.model.strategy_module import StrategyModule
from stsdk.utils.log import log


class ST1(StrategyModule):
    name = "ST1"

    def init_params(self):
        log.info("ST1 init_params")
        self.register(
            DMS_BBO,
            self.handle_bbo,
            instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        )
        self.register(
            OMS_ORDER_UPDATE,
            self.handle_order_update,
            strategy_id="2",
            account_id="yangwang_account_binance01",
        )

    def start_trading_session(self):
        pass

    def run_on_data_feed(self, *args):
        pass

    def handle_bbo(self, message):
        log.info("bbo: %s" % message)
        self.place_order_signal(
            "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
            "1000",
            "1",
            "buy",
            "OPEN",
        )

    def handle_order_update(self, message):
        log.info(message)


async def main():
    st = ST1("2", "yangwang_account_binance01")
    # if __name__ == '__main__':
    # st = ST1("17", "test-future")
    # ST1("4", "aris_lingxiao_test")
    # resp = st.place_order(
    #     "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
    #     "1000",
    #     "1",
    #     "buy",
    #     "OPEN",
    # )
    # if "orderId" in resp:
    #     print("success place order, order id is", resp["orderId"])
    # else:
    #     print("fail to place order, resp is", resp)
    # # print(st.get_all_open_orders())
    # time.sleep(30)
    # print("main --------------------------------------")
    # resp = st.cancel_order(resp["instrumentId"], resp["orderId"])
    # if "orderId" in resp:
    #     print("success cancel order, order id is", resp["orderId"])
    # else:
    #     print("fail to cancel order, resp is", resp)
    # print(st.get_all_open_orders())
    # print("main --------------------------------------")
    # print(st.get_all_positions())


if __name__ == "__main__":
    asyncio.run(main())
