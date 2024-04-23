import asyncio
import time

from stsdk.common.env import ENV_TEST
from stsdk.common.key import DMS_BBO, OMS_ORDER_UPDATE
from stsdk.model.strategy_module import StrategyModule
from stsdk.utils.config import config
from stsdk.utils.log import log
# from stsdk.utils.metric import metric


class ST2(StrategyModule):
    name = "ST2"

    def init_params(self):
        log.info(f"init_params {self.name}")
        # 设置测试环境
        config.set_env(ENV_TEST)
        # 注册 DMS_BBO 和 OMS_ORDER_UPDATE 事件，并指定相应的处理函数
        # self.register(
        #     DMS_BBO,
        #     # self.handle_bbo,
        #     instrument_id="EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED",
        # )
        # self.register(
        #     OMS_ORDER_UPDATE,
        #     # self.handle_order_update,
        #     strategy_id=self.strategy_id,
        #     account_id=self.account_id,
        # )
    # def handle_bbo(self, message):
    #     metric.MetricTime(
    #         "ws_oms_stsdk", message["topic"], message["tt"] / 1000000, time.time()
    #     )
    # def handle_order_update(self, message):
    #     log.info("order update", message)
    #     body = message["body"]
    #     order_id = body["order_id"]
    #     instrument_id = body["instrument_id"]
    #     log.info(f"order_id: {order_id}, instrument_id: {instrument_id}")

    # def get_open_orders_test(self):
    #     pass

async def main():
    st = ST2("1", "aris_test")
    # st.get_position("EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    report=st.get_open_orders("EXCHANGE_BINANCE.ETH-USDT.SECURITY_TYPE_PERP.CONTRACT_TYPE_LINEAR.USDT.UNSPECIFIED")
    log.info(report)

if __name__ == "__main__":
    asyncio.run(main())