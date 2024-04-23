import asyncio
import sys
import time

sys.path.append("/root/lingxiao/st-sdk/")
sys.path.append("/root/lingxiao/st-sdk/stsdk")

from stsdk.common.key import DMS_BBO, OMS_ORDER_UPDATE
from stsdk.model.strategy_module import StrategyModule


class ST1(StrategyModule):
    name = "signal_order"

    def init_params(self):
        print("ST1 init_params")
        self.register(
            DMS_BBO,
            self.handle_bbo,
            "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        )
        self.register(
            OMS_ORDER_UPDATE,
            self.handle_order_update,
            self.strategy_id,
            self.account_id,
        )

    def start_trading_session(self):
        pass

    def run_on_data_feed(self, *args):
        pass

    def handle_error(self, error):
        print("error", error)

    def handle_bbo(self, message):
        print("bbo", message)
        # resp = self.place_order(
        #     "EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        #     "1000",
        #     "1",
        #     "buy",
        #     "OPEN",
        # )
        # print(resp)

    def handle_order_update(self, message):
        print(message)


async def main():
    st = ST1("2", "yangwang_account_binance01")
    time.sleep(1)
    # if __name__ == '__main__':
    # st = ST1("17", "test-future")
    ST1("4", "aris_lingxiao_test")
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
